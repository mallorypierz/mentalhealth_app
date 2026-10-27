import test from 'node:test';
import assert from 'node:assert/strict';
import { VoiceSession } from '../src/voiceSession.js';
function fixture() {
  let access = { access_token: 'fake-test-token', context_version: 2 }, counter = 0;
  const sockets = [], states = [], calls = [];
  let session = { id: 'session', revision: 1, state: 'ready', turns: [] };
  const voice = new VoiceSession({
    api: async (url, method, body) => { calls.push({ url, method, body }); return session; },
    access: () => access, uuid: () => `test-${++counter}`,
    socket: () => { const ws = { readyState: 0, sent: [], send(value) { this.sent.push(JSON.parse(value)); }, close() { this.readyState = 3; } }; sockets.push(ws); return ws; },
    changed: state => states.push(state), messages: () => {},
  });
  return { voice, sockets, states, calls, setAccess: value => { access = value; }, setSession: value => { session = value; } };
}
test('explicit start only, fixed automatic turn submission and duplicate click guard', async () => {
  const f = fixture(); assert.equal(f.sockets.length, 0);
  await f.voice.start('conversation'); await f.voice.start('conversation');
  assert.equal(f.calls.length, 1); assert.equal(f.sockets.length, 1);
  const ws = f.sockets[0]; ws.readyState = 1; ws.onopen();
  assert.equal(ws.sent[0].type, 'authenticate');
  await ws.onmessage({ data: JSON.stringify({ type: 'ready' }) });
  assert.equal(ws.sent[1].type, 'mock_turn'); assert.equal(f.voice.state.microphone, 'off');
  await ws.onmessage({ data: JSON.stringify({ type: 'transcript', text: 'fixed fictional question' }) });
  assert.equal(f.voice.state.transcript, 'fixed fictional question'); assert.equal(f.voice.state.phase, 'processing');
});
test('late events cannot change view after stop or profile change', async () => {
  const f = fixture(); await f.voice.start('conversation'); const ws = f.sockets[0];
  await f.voice.stop(); const count = f.states.length;
  await ws.onmessage({ data: JSON.stringify({ type: 'transcript', text: 'stale text' }) });
  assert.equal(f.states.length, count); assert.equal(f.voice.state.phase, 'stopped');
  await f.voice.start('conversation'); const second = f.sockets[1];
  f.setAccess({ access_token: 'other-profile', context_version: 3 });
  await second.onmessage({ data: JSON.stringify({ type: 'transcript', text: 'wrong owner' }) });
  assert.notEqual(f.voice.state.transcript, 'wrong owner');
});
test('speech failure does not turn a saved reply into a failed save', async () => {
  const f = fixture(); await f.voice.start('conversation');
  const turn = { id: 'turn', state: 'completed', submission: 'saved', speech: 'failed', error_code: 'speech_failed', request: { assistant_persistence: 'saved' } };
  f.setSession({ id: 'session', state: 'active', revision: 2, turns: [turn] });
  await f.voice.refresh();
  assert.equal(f.voice.state.turn.request.assistant_persistence, 'saved');
  assert.equal(f.voice.state.turn.speech, 'failed'); assert.match(f.voice.state.error, /speech failed/);
});
test('next automatic mock turn continues to accept events on the same socket', async () => {
  const f = fixture(); await f.voice.start('conversation'); const ws = f.sockets[0]; ws.readyState = 1;
  await ws.onmessage({ data: JSON.stringify({ type: 'ready' }) });
  f.setSession({ id: 'session', state: 'active', revision: 2, turns: [{ state: 'completed' }] });
  await f.voice.refresh(); await f.voice.start('conversation');
  await ws.onmessage({ data: JSON.stringify({ type: 'transcript', text: 'second transcript' }) });
  assert.equal(f.voice.state.transcript, 'second transcript'); assert.equal(f.sockets.length, 1);
});

test('provisional recognition concern stops transport and holds words without claiming a save', async () => {
  const f = fixture(); await f.voice.start('conversation'); const ws = f.sockets[0]; ws.readyState = 1;
  await ws.onmessage({ data:JSON.stringify({type:'transcript_partial',text:'Fictional: I might do something to myself'}) });
  assert.equal(ws.readyState,3); assert.equal(f.voice.state.phase,'held');
  assert.equal(f.voice.state.support,true); assert.equal(f.voice.state.submissionEvidence,'unknown');
  const count=ws.sent.length;
  await ws.onmessage({data:JSON.stringify({type:'ready'})});
  assert.equal(ws.sent.length,count); // no silent restart from a late event
});

test('server-confirmed held transcript keeps not-saved distinct from uncertainty', async () => {
  const f = fixture(); await f.voice.start('conversation'); const ws=f.sockets[0];
  await ws.onmessage({data:JSON.stringify({type:'support_notice',text:"I don't want to be alive",submission:'not_saved'})});
  assert.equal(f.voice.state.submissionEvidence,'not_saved');
  assert.equal(f.voice.state.microphone,'off'); assert.equal(f.voice.state.phase,'held');
});

test('live transport accepts one audio turn, waits during processing and rejects late submission after stop',async()=>{
 const f=fixture(); await f.voice.start('conversation',true);const ws=f.sockets[0];ws.readyState=1;ws.onopen();
 await ws.onmessage({data:JSON.stringify({type:'ready',provider:'openai'})});
 assert.equal(ws.sent.length,1); assert.equal(f.voice.state.phase,'listening');
 assert.equal(f.voice.sendAudio(new Uint8Array([1,2,3])),true);
 assert.equal(ws.sent[1].type,'audio_turn'); assert.equal(ws.sent[1].audio,'AQID');
 assert.equal(f.voice.sendAudio(new Uint8Array([1])),false);
 await f.voice.stop(); assert.equal(f.voice.sendAudio(new Uint8Array([1])),false);
});
test('live start refuses a mock backend instead of sending microphone audio',async()=>{
 const f=fixture();await f.voice.start('conversation',true); const ws=f.sockets[0];ws.readyState=1;
 await ws.onmessage({data:JSON.stringify({type:'ready',provider:'mock'})});
 assert.equal(f.voice.state.phase,'failed');assert.equal(ws.sent.length,0);
 assert.equal(f.voice.sendAudio(new Uint8Array([1])),false);
});

test('restoring voice controls never opens microphone/socket and ignores a late owner response',async()=>{
 const f=fixture(); await f.voice.restore('conversation');
 assert.equal(f.sockets.length,0);assert.equal(f.voice.state.microphone,'off');assert.equal(f.voice.state.historical,true);
 assert.equal(f.calls[0].url,'/voice/conversations/conversation/latest-turn');
 let resolve; f.voice.api=()=>new Promise(r=>resolve=r);
 const restoring=f.voice.restore('other');f.setAccess({access_token:'different',context_version:4});
 resolve({turn:{id:'wrong-owner'}});await restoring;
 assert.equal(f.voice.state.turn,null);
});


test('budget failure accurately reports whether the message was saved',async()=>{
 const f=fixture(); f.voice.session={id:'session'};
 for(const submission of ['not_saved','saved','unknown']) {
  f.voice.api=async()=>({id:'session',turns:[{state:'failed',submission,error_code:'budget_exhausted'}]});
  await f.voice.refresh();
  assert.match(f.voice.state.error, submission==='not_saved' ? /Your message was not saved/ : submission==='saved' ? /Your message was saved/ : /Save status is unknown/);
 }
});
