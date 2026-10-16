export const DURATION = 60000;
export class Exercise {
  constructor(now = () => performance.now()) { this.now = now; this.state = 'ready'; this.elapsed = 0; this.anchor = 0; }
  start() { this.elapsed = 0; this.anchor = this.now(); this.state = 'running'; }
  tick() {
    if (this.state === 'running') {
      const time = this.now(); this.elapsed = Math.min(DURATION, this.elapsed + time - this.anchor); this.anchor = time;
      if (this.elapsed >= DURATION) this.state = 'completed';
    }
    return this.snapshot();
  }
  pause() { this.tick(); if (this.state === 'running') this.state = 'paused'; }
  resume() { if (this.state === 'paused') { this.anchor = this.now(); this.state = 'running'; } }
  stop() { this.tick(); if (['running', 'paused'].includes(this.state)) this.state = 'stopped'; }
  snapshot() {
    const within = this.elapsed % 10000;
    return { state: this.state, elapsed: this.elapsed, cycle: Math.min(6, Math.floor(this.elapsed / 10000) + 1), phase: within < 4000 ? 'Breathe in' : 'Breathe out', count: within < 4000 ? 4 - Math.floor(within / 1000) : 6 - Math.floor((within - 4000) / 1000), remaining: Math.ceil((DURATION - this.elapsed) / 1000) };
  }
}
export class LatestRequest {
  version = 0;
  cancel() { this.version++; }
  async run(work, apply) {
    const version = ++this.version;
    try { const value = await work(); if (version === this.version) apply({ value }); }
    catch (error) { if (version === this.version) apply({ error }); }
  }
}
