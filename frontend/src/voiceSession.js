import { matchesCrisisPhrase } from './crisis.js';
// Transport coordinator; microphone capture is separately and explicitly started.
export class VoiceSession {
  constructor({ api, access, socket, changed, messages, uuid = () => crypto.randomUUID() }) {
    Object.assign(this, { api, access, socketFactory: socket, changed, messages, uuid });
    this.live=false; this.heartbeat=null;
    this.epoch = 0; this.ws = null; this.session = null; this.creation = null;
    this.state = { phase: 'ready', transcript: '', turn: null, error: '', microphone: 'off', support: false, submissionEvidence: null };
  }
  publish(value) { this.state = { ...this.state, ...value }; this.changed(this.state); }
  current(epoch, access) { return epoch === this.epoch && access === this.access(); }
  async start(conversation, live=false) {
    this.live=live;
    if (['connecting', 'listening', 'processing'].includes(this.state.phase)) return;
    const epoch = this.ws?.readyState === 1 ? this.epoch : ++this.epoch, access = this.access();
    this.publish({ phase: 'connecting', historical:false, error: '', transcript: '', turn: null, support: false, submissionEvidence: null });
    try {
      if (!this.session) {
        this.creation ||= { session_id: this.uuid(), conversation_id: conversation, operation_id: this.uuid() };
        const session = await this.api('/voice/sessions', 'POST', this.creation);
        if (!this.current(epoch, access)) {
          if (access === this.access()) await this.api(`/voice/sessions/${session.id}/stop`, 'POST', { operation_id: this.uuid(), expected_revision: session.revision });
          return;
        }
        this.session = session; this.creation = null;
      }
      if (this.ws?.readyState === 1) { if(!this.live) this.sendTurn(); return; }
      const ws = this.socketFactory(); this.ws = ws;
      ws.onopen = () => {
        if (!this.current(epoch, access)) { ws.close(); return; }
        ws.send(JSON.stringify({ type: 'authenticate', token: access.access_token, context_version: access.context_version, session_id: this.session.id }));
      };
      ws.onmessage = async event => {
        if (!this.current(epoch, access)) return;
        let data;
        try { data = JSON.parse(event.data); } catch { this.publish({ error: 'Invalid voice response.', phase: 'failed' }); ws.close(); return; }
        if (data.type === 'support_notice') { await this.holdForSupport(data.text || this.state.transcript, data.submission === 'not_saved'); return; }
        if (['transcript', 'transcript_partial'].includes(data.type) && matchesCrisisPhrase(data.text || '')) {
          await this.holdForSupport(data.text, false); return;
        }
        if (data.type === 'transcript_partial') this.publish({ transcript: data.text });
        if (data.type === 'ready') {
          if(this.live && data.provider!=='openai') { await this.stop(); this.publish({phase:'failed',error:'Live voice is disabled. No microphone audio was sent.'}); return; }
          if(this.live) { this.publish({phase:'listening',microphone:'on'}); this.heartbeat=setInterval(()=>{ if(ws.readyState===1) ws.send(JSON.stringify({type:'ping'})); },20000); }
          else this.sendTurn();
        }
        if (data.type === 'transcript') this.publish({ transcript: data.text, phase: 'processing' });
        if (data.type === 'submitted') this.messages();
        if (data.type === 'status') await this.refresh(epoch, access);
        if (data.type === 'stopped') this.publish({ phase: 'stopped', error: '' });
        if (data.type === 'error') this.publish({ phase: 'failed', error: data.message });
      };
      ws.onerror = () => { if (this.current(epoch, access)) this.publish({ phase: 'failed', error: 'Voice connection failed. Check saved history; no automatic retry.' }); };
      ws.onclose = () => {
        if (!this.current(epoch, access)) return;
        clearInterval(this.heartbeat); this.session = null; this.ws = null;
        this.publish({ phase: 'stopped', error: this.state.error || 'Voice session ended. Start again explicitly.' });
        this.messages();
      };
    } catch (error) {
      if (this.current(epoch, access)) this.publish({ phase: 'failed', error: error.message || 'Voice session save is not confirmed.' });
    }
  }
  async holdForSupport(text, confirmedNotSubmitted) {
    this.publish({ support:true, transcript:text, submissionEvidence:confirmedNotSubmitted ? 'not_saved' : 'unknown' });
    const access=this.access(), stopping=this.stop(), epoch=this.epoch;
    await stopping;
    if (this.current(epoch,access)) this.publish({ phase:'held', microphone:'off' });
  }
  sendTurn() {
    const body = { type: 'mock_turn', turn_id: this.uuid(), request_id: this.uuid(), operation_id: this.uuid(), scenario: 'success' };
    this.publish({ phase: 'listening', transcript: '', turn: null });
    this.ws.send(JSON.stringify(body));
  }
  sendAudio(bytes) {
    if(!this.live || this.ws?.readyState!==1 || !['listening','ready'].includes(this.state.phase)) return false;
    let binary='';
    for(let i=0;i<bytes.length;i+=8192) binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
    this.speechRetry=null;
    this.publish({phase:'processing', transcript:'',turn:null});
    this.ws.send(JSON.stringify({type:'audio_turn',turn_id:this.uuid(),request_id:this.uuid(),operation_id:this.uuid(),audio:btoa(binary)}));
    return true;
  }
  async refresh(epoch = this.epoch, access = this.access()) {
    const id = this.session?.id;
    if (!id) return;
    try {
      const session = await this.api(`/voice/sessions/${id}`);
      if (!this.current(epoch, access)) return;
      this.session = session;
      const turn = session.turns.at(-1);
      if (turn) this.publish({ turn, phase: turn.state === 'processing' ? 'processing' : turn.state === 'completed' ? 'ready' : turn.state,
        error: turn.error_code ? `Voice turn: ${turn.error_code.replaceAll('_', ' ')}. ${turn.submission === 'not_saved' ? 'Your message was not saved.' : turn.submission === 'saved' ? 'Your message was saved. Check the conversation below.' : 'Save status is unknown. Check history before retrying.'}` : '' });
      if (turn?.error_code === 'support_notice') {
        this.publish({ support:true, submissionEvidence:turn.request?.user_persistence === 'saved' ? 'saved' : 'not_saved' });
        await this.stop();
      }
      this.messages();
    } catch {
      if (this.current(epoch, access)) this.publish({ phase: 'failed', error: 'Voice save status is unknown. Check history before retrying.' });
    }
  }
  async restore(conversation) {
    const epoch=++this.epoch, access=this.access();
    this.speechRetry=null;
    this.publish({turn:null,transcript:'',phase:'stopped',microphone:'off',historical:true,error:'',support:false});
    try {
      const result=await this.api(`/voice/conversations/${conversation}/latest-turn`);
      if(!this.current(epoch,access)) return;
      this.publish({turn:result.turn,historical:true,error:result.turn?.speech==='failed' ? 'Reply audio failed. The text reply is saved; you can retry audio.' : ''});
    } catch { if(this.current(epoch,access)) this.publish({error:'Saved voice controls could not load. The conversation text remains available.'}); }
  }
  async retrySpeech() {
    const turn=this.state.turn, epoch=this.epoch, access=this.access();
    if(!turn || turn.request?.assistant_persistence!=='saved') return;
    this.speechRetry ||= {action:'retry_speech',operation_id:this.uuid(),expected_revision:turn.revision};
    try {
      const result=await this.api(`/voice/turns/${turn.id}/actions`,'POST',this.speechRetry);
      if(!this.current(epoch,access)) return;
      this.speechRetry=null;
      this.publish({turn:result,error:result.error_code || '',phase:'ready'});
    } catch { if(this.current(epoch,access)) this.publish({error:'Speech retry was not confirmed. Retry keeps the same operation; the saved text is unchanged.'}); }
  }
  async retrySave() {
    const turn=this.state.turn, epoch=this.epoch, access=this.access();
    if (!turn || turn.error_code!=='reply_save_failed') return;
    try {
      const result=await this.api(`/voice/turns/${turn.id}/actions`, 'POST', { action:'retry_reply_save', operation_id:this.uuid(), expected_revision:turn.revision });
      if (!this.current(epoch,access)) return;
      this.publish({ turn:result, phase:'ready', error:'' }); this.messages();
    } catch { if (this.current(epoch,access)) this.publish({ error:'Reply save is not confirmed or the temporary reply expired. Check history.' }); }
  }
  async stop() {
    clearInterval(this.heartbeat);
    const session = this.session, access = this.access();
    ++this.epoch;
    this.ws?.close(); this.ws = null;
    this.publish({ phase: 'stopped', microphone: 'off' });
    if (!session) return true;
    try {
      // Connection closure also stops the backend session; reconcile its latest revision.
      const latest = await this.api(`/voice/sessions/${session.id}`);
      if (access !== this.access()) return false;
      if (['ready', 'active'].includes(latest.state)) await this.api(`/voice/sessions/${session.id}/stop`, 'POST', { operation_id: this.uuid(), expected_revision: latest.revision });
      this.session = null; this.creation = null;
      return true;
    } catch {
      this.publish({ error: 'Stopping could not be confirmed. Retry End conversation before switching profiles.' });
      return false;
    }
  }
}
