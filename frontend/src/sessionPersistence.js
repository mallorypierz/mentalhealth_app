import { ownerKey } from './identityAccess.js';
import { api } from './api.js';
const PREFIX = 'coursework-session-outbox:';
const uuid = () => crypto.randomUUID();

// This browser journal stores pending operations, not the displayed history.
// SQLite remains authoritative. Per-session Web Locks protect live tabs.
export class SessionPersistence {
  constructor(notify) { this.prefix = PREFIX + ownerKey() + ':'; this.notify = notify; this.jobs = new Map(); }
  persist(job) {
    try { localStorage.setItem(this.prefix + job.id, JSON.stringify(job.data)); }
    catch { job.journalFailed = true; }
  }
  report(job, state, message) {
    job.state = state;
    this.notify({ id: job.id, state, message: message + (job.journalFailed ? ' Browser recovery unavailable; keep this tab open to retry.' : '') });
  }
  async begin(id, started) {
    const job = { id, data: { create: { session_id: id, operation_id: uuid(), owner_token: uuid(), skill_key: 'paced_breathing_4_6', started_at: started }, saved: null, pending: null, desired: null }, busy: false };
    this.jobs.set(id, job);
    this.persist(job);
    if (navigator.locks) {
      await new Promise(resolve => navigator.locks.request(this.prefix + id, async () => {
        resolve(); await new Promise(release => { job.release = release; });
      }));
    } else { job.journalFailed = true; }
    this.flush(job);
  }
  checkpoint(id, snapshot, ended = null) {
    const job = this.jobs.get(id);
    if (!job) return;
    job.data.desired = {
      status: ['completed', 'stopped'].includes(snapshot.state) ? snapshot.state : 'in_progress',
      active_duration_ms: Math.floor(snapshot.elapsed), paused_duration_ms: Math.floor(snapshot.paused), ended_at: ended,
    };
    this.persist(job);
    // Once a save has failed, explicit Retry resumes work; cues remain independent.
    if (!['failed', 'unknown'].includes(job.state)) this.flush(job);
  }
  async flush(job) {
    if (job.busy) return;
    job.busy = true;
    this.report(job, 'saving', 'Saving session…');
    try {
      if (!job.data.saved) {
        job.data.saved = (await api('/sessions', 'POST', job.data.create)).session;
        this.persist(job);
      }
      while (job.data.pending || job.data.desired) {
        if (!job.data.pending) {
          job.data.pending = { operation_id: uuid(), owner_token: job.data.create.owner_token, expected_revision: job.data.saved.revision, ...job.data.desired };
          job.data.desired = null;
          this.persist(job); // Preserve exact operation across lost responses/reloads.
        }
        job.data.saved = (await api(`/sessions/${job.id}`, 'PUT', job.data.pending)).session;
        job.data.pending = null;
        this.persist(job);
        if (job.data.saved.status !== 'in_progress') { job.data.desired = null; break; }
      }
      this.report(job, 'saved', job.data.saved.status === 'in_progress' ? 'Latest checkpoint saved.' : 'Session saved.');
      if (job.data.saved.status !== 'in_progress') {
        localStorage.removeItem(this.prefix + job.id); job.release?.();
      }
    } catch (error) {
      this.report(job, error.persistence === 'unknown' ? 'unknown' : 'failed',
        error.persistence === 'unknown' ? 'Save not confirmed. Retry to check and save safely.' : `Save failed. ${error.message}`);
    } finally { job.busy = false; }
  }
  async settle() {
    const deadline = Date.now() + 6000;
    while ([...this.jobs.values()].some(job => job.busy) && Date.now() < deadline) await new Promise(resolve => setTimeout(resolve, 50));
    if ([...this.jobs.values()].some(job => job.busy || ['failed', 'unknown'].includes(job.state))) throw new Error('Retry the session save before switching.');
  }
  retry(id) { const job = this.jobs.get(id); if (job?.recovering) this.recover(); else if (job) this.flush(job); }
  async recover() {
    if (!navigator.locks) return;
    const keys = Object.keys(localStorage).filter(key => key.startsWith(this.prefix));
    await Promise.all(keys.map(key => navigator.locks.request(key, { ifAvailable: true }, async lock => {
      if (!lock) return; // A live tab owns this practice, including its failed saves.
      const raw = localStorage.getItem(key);
      if (!raw) return;
      let data;
      try { data = JSON.parse(raw); } catch { return; }
      const job = { id: key.slice(this.prefix.length), data, busy: false, recovering: true };
      this.jobs.set(job.id, job);
      try {
        let saved;
        try { saved = (await api(`/sessions/${job.id}`)).session; }
        catch (error) { if (error.status !== 404) throw error; saved = (await api('/sessions', 'POST', data.create)).session; }
        data.saved = saved;
        if (saved.status !== 'in_progress') {
          localStorage.removeItem(key); this.report(job, 'saved', 'Saved session recovered.'); return;
        }
        // A genuinely finished local session can retry its original final write.
        if (data.desired?.status === 'completed' || data.desired?.status === 'stopped' ||
            data.pending?.status === 'completed' || data.pending?.status === 'stopped') {
          await this.flush(job); return;
        }
        // GET is authoritative after an abandoned practice. Discard unsent
        // checkpoints instead of extending its last confirmed saved duration.
        data.saved = saved; data.pending = null;
        data.desired = { status: 'interrupted', active_duration_ms: saved.active_duration_ms,
          paused_duration_ms: saved.paused_duration_ms, ended_at: new Date().toISOString() };
        this.persist(job); await this.flush(job);
      } catch (error) { this.report(job, 'unknown', 'Previous session recovery failed. Retry when the backend is available.'); }
    })));
  }
}
