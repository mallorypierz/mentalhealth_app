<script setup>
import { getAccess, ownerKey } from '../identityAccess.js';
import { computed, onMounted, onUnmounted, ref, watch, nextTick } from 'vue';
import { api } from '../api.js';
import { Microphone, acceptsMicrophoneInput } from '../microphone.js';
import { VoiceSession } from '../voiceSession.js';
import { matchesCrisisPhrase, CRISIS_NOTICE, DETECTION_LIMITS } from '../crisis.js';
function displayedMessage(message) {
  if (message.role !== 'assistant' || message.provider !== 'mock') return message.content;
  // Presentation only: retain the original reply and citation in the API/database.
  return message.content.replace(/Record \[[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\]\. ?/gi, '');
}
const emit = defineEmits(['support']);
const props = defineProps({ suspended: Boolean });
const crisisNotice = ref('');
const matchingDraft = computed(() => matchesCrisisPhrase(draft.value));
const conversations = ref([]), conversationCursor = ref(null), listState = ref('loading');
const selected = ref(''), messages = ref([]), messageCursor = ref(null), messageState = ref('idle');
const draft = ref(''), mode = ref('success'), request = ref(null), busy = ref(false), notice = ref('');
// Reverse request groups, not individual messages: each question stays above its reply.
const messageGroups = computed(() => {
  const groups = new Map();
  for (const message of [...messages.value].sort((a, b) => a.sequence - b.sequence)) {
    if (!groups.has(message.request_id)) groups.set(message.request_id, { id: message.request_id, sequence: message.sequence, messages: [] });
    groups.get(message.request_id).messages.push(message);
  }
  return [...groups.values()].sort((a, b) => b.sequence - a.sequence);
});
const configuration = ref(null);
const liveVoice = computed(() => configuration.value?.voice_enabled === true);
const uncertain = ref(null), storageWarning = ref('');
let epoch = 0, pollTimer, disposed = false, listEpoch = 0;
const pending = computed(() => busy.value || request.value?.status === 'pending' || !!uncertain.value || ['permission','connecting', 'listening', 'processing'].includes(voiceState.value.phase));
const errorText = computed(() => ({
  support_notice: request.value?.failure_stage === 'response_review' ? 'The generated reply was withheld. Your message remains saved. Crisis support is available.' : 'This saved message was not sent for another AI answer. Crisis support is available.',
  configuration_unavailable: 'Live chat is not configured. Practice and support remain available.',
  budget_exhausted: 'The approved live-call budget is exhausted. No new call was sent.',
  provider_http_401: 'Provider authentication failed. Check the local key configuration; no assistant reply was saved.',
  provider_http_429: 'The provider reported a rate or quota limit. No assistant reply was saved.',
  provider_connection_failure: 'The provider connection failed. No assistant reply was saved.',
  provider_refusal: 'The provider declined this request. No assistant reply was saved.',
  rejected_query: 'The proposed retrieval query was rejected. No assistant reply was generated.',
  database_error: 'History retrieval failed. This is not empty history; no assistant reply was generated.',
  query_timeout: 'History retrieval exceeded its time limit. No assistant reply was generated.',
  provider_failure: 'The provider failed. Your message is saved; no assistant reply was created.',
  provider_timeout: 'The provider timed out. Your message is saved; no assistant reply was created.',
  reply_save_failed: 'Reply save failed. Your message is saved, but no assistant reply is saved. Retry generates a new reply.',
  interrupted: 'The request was interrupted. Your message is saved; no assistant reply was saved. Retry when you choose.',
  response_unavailable: 'This reply could not be provided within this app’s educational scope. Your message remains saved. You can use reviewed practice or Crisis support.',
  invalid_provider_output: 'The provider returned an invalid response. No assistant reply was saved.',
}[request.value?.error_code] || 'Request failed. No assistant reply is saved.'));
const journalKey = id => `coursework-chat-pending:${id}`;
function readJournal(id) { try { return JSON.parse(sessionStorage.getItem(ownerKey() + ':' + journalKey(id)) || 'null'); } catch { return null; } }
function writeJournal(id, body) {
  try { if (body) sessionStorage.setItem(ownerKey() + ':' + journalKey(id), JSON.stringify(body)); else sessionStorage.removeItem(ownerKey() + ':' + journalKey(id)); }
  catch { storageWarning.value = 'Browser retry storage is unavailable. Keep this tab open until submission is confirmed.'; }
}
async function loadConversations(more = false) {
  const version = ++listEpoch;
  listState.value = 'loading';
  try {
    const value = await api(`/conversations?cursor=${more ? conversationCursor.value : 0}`);
    if (disposed || version !== listEpoch) return;
    conversations.value = more ? [...conversations.value, ...value.conversations] : value.conversations;
    conversationCursor.value = value.next_cursor; listState.value = 'success';
  } catch { if (!disposed && version === listEpoch) listState.value = 'failed'; }
}
async function refreshMessages(version = epoch, more = false) {
  const id = selected.value;
  if (!id) return;
  try {
    const value = await api(`/conversations/${id}/messages?cursor=${more ? messageCursor.value : 0}&limit=100`);
    if (disposed || version !== epoch) return;
    // The API is oldest-first. Read remaining pages before presenting newest pairs.
    while (value.next_cursor !== null) {
      const page = await api(`/conversations/${id}/messages?cursor=${value.next_cursor}&limit=100`);
      if (disposed || version !== epoch) return;
      value.messages.push(...page.messages);
      value.next_cursor = page.next_cursor;
      value.latest_request_id = page.latest_request_id;
    }
    messages.value = more ? [...messages.value, ...value.messages] : value.messages;
    messageCursor.value = value.next_cursor; messageState.value = 'success';
    // Persisted request state reconstructs pending/failed UI after reload.
    if (!request.value && value.latest_request_id) await poll(value.latest_request_id, version);
  } catch { if (!disposed && version === epoch) messageState.value = 'failed'; }
}
async function poll(id, version) {
  try {
    const value = await api(`/requests/${id}`);
    if (disposed || version !== epoch) return;
    const changed = request.value?.status !== value.status;
    request.value = value;
    if (value.status === 'pending') pollTimer = setTimeout(() => poll(id, version), 500);
    else if (changed) await refreshMessages(version);
  } catch {
    if (disposed || version !== epoch) return;
    notice.value = 'Request status could not be checked. Its save state is unknown; refresh status before retrying.';
    // No automatic resubmission or invented reply after a lost connection.
  }
}
async function selectConversation(id) {
  stopSpeaking();
  if (voice.session && !await voice.stop()) return;
  const version = ++epoch; clearTimeout(pollTimer);
  crisisNotice.value = '';
  selected.value = id; messages.value = []; messageCursor.value = null; request.value = null;
  messageState.value = 'loading'; notice.value = ''; busy.value = false;
  uncertain.value = readJournal(id); draft.value = uncertain.value?.content || '';
  await refreshMessages(version);
  if (version !== epoch || disposed) return;
  await voice.restore(id);
  if (version !== epoch || !uncertain.value) return;
  const pendingBody = uncertain.value;
  try {
    const value = await api(`/requests/${pendingBody.request_id}`);
    if (version !== epoch || disposed) return;
    request.value = value; uncertain.value = null; writeJournal(id, null); draft.value = '';
    if (value.status === 'pending') { clearTimeout(pollTimer); pollTimer = setTimeout(() => poll(value.id, version), 500); }
  } catch { if (version === epoch) notice.value = 'Submission is not confirmed. Retry the original submission safely.'; }
}
async function newConversation() {
  if (busy.value) return;
  stopSpeaking();
  if (voice.session && !await voice.stop()) return;
  const version = ++epoch; clearTimeout(pollTimer); busy.value = true; notice.value = '';
  let body = readJournal('new-conversation');
  if (!body) { body = { conversation_id: crypto.randomUUID(), operation_id: crypto.randomUUID() }; writeJournal('new-conversation', body); }
  try {
    const value = await api('/conversations', 'POST', body);
    writeJournal('new-conversation', null);
    if (disposed || version !== epoch) return;
    await loadConversations();
    if (disposed || version !== epoch) return;
    await selectConversation(value.id);
  } catch { if (version === epoch) notice.value = 'Conversation save failed or was not confirmed. New conversation retries the same operation.'; }
  finally { if (version === epoch) busy.value = false; }
}
async function submit(replay = false) {
  if (busy.value || !selected.value || request.value?.status === 'pending') return;
  if (!replay && (uncertain.value || !draft.value.trim())) return;
  const content = replay ? uncertain.value?.content : draft.value;
  if (matchesCrisisPhrase(content || '')) {
    crisisNotice.value = replay
      ? 'No new AI request was sent. Check saved history for any earlier submission. Crisis support is available.'
      : CRISIS_NOTICE;
    return;
  }
  crisisNotice.value = '';
  if (voiceState.value.support) voice.publish({ support:false, submissionEvidence:null, transcript:'' });
  const id = selected.value, version = ++epoch; clearTimeout(pollTimer);
  const body = replay ? uncertain.value : { request_id: crypto.randomUUID(), content: draft.value, mock_mode: mode.value };
  if (!body) return;
  request.value = null;
  uncertain.value = body; writeJournal(id, body); busy.value = true; notice.value = 'Saving your message…';
  try {
    const value = await api(`/conversations/${id}/messages`, 'POST', body);
    writeJournal(id, null);
    if (disposed || version !== epoch) return;
    uncertain.value = null; draft.value = ''; request.value = value; notice.value = '';
    await refreshMessages(version);
    if (version === epoch) { clearTimeout(pollTimer); await poll(value.id, version); }
  } catch (error) {
    if (disposed || version !== epoch) return;
    notice.value = error.status === 422 ? 'Message rejected. Check the text; it was not submitted.' :
      'Message save failed or was not confirmed. Retry uses the same request ID and text.';
    if (error.status === 422) { uncertain.value = null; writeJournal(id, null); }
  } finally { if (version === epoch) busy.value = false; }
}
async function retryReply() {
  if (busy.value || request.value?.status !== 'failed') return;
  const id = request.value.id, version = ++epoch; clearTimeout(pollTimer); busy.value = true; notice.value = '';
  const key = `retry-${id}`;
  const body = readJournal(key) || { operation_id: crypto.randomUUID(), mock_mode: mode.value };
  writeJournal(key, body);
  try {
    const value = await api(`/requests/${id}/retry`, 'POST', body);
    writeJournal(key, null);
    if (disposed || version !== epoch) return;
    request.value = value; await refreshMessages(version); await poll(id, version);
  } catch { if (version === epoch) notice.value = 'Retry was not confirmed. Check status or repeat this same retry safely.'; }
  finally { if (version === epoch) busy.value = false; }
}
const voiceState = ref({ phase: 'ready', transcript: '', turn: null, error: '', microphone: 'off' });
const autoPlay = ref(true), playback = ref('idle');
let audio, audioURL, playbackEpoch = 0, lastPlayed = '';
const voice = new VoiceSession({
  api, access: getAccess,
  socket: () => new WebSocket(`${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}/api/voice/stream`),
  changed: state => {
    voiceState.value = { ...state };
    if (['stopped','failed','held'].includes(state.phase)) microphone.stop();
    if (state.support) { stopSpeaking(); crisisNotice.value = CRISIS_NOTICE; }
    if (!state.historical && state.turn?.speech === 'ready' && state.turn.id !== lastPlayed && autoPlay.value && !props.suspended && !document.hidden) {
      lastPlayed = state.turn.id; playMockAudio();
    }
  },
  messages: async () => {
    if (disposed) return;
    request.value = null; await refreshMessages(epoch);
  },
});
const microphone = new Microphone({
  send: bytes => voice.sendAudio(bytes),
  onset: () => {}, // Playback is interrupted only by explicit controls or leaving the page.
  accepting: () => acceptsMicrophoneInput({live:liveVoice.value, phase:voice.state.phase, playback:playback.value, suspended:props.suspended, hidden:document.hidden}),
  failed: message => { endVoice(); voice.publish({phase:'failed',error:message}); },
});
function stopSpeaking() {
  ++playbackEpoch;
  if (audio) { audio.pause(); audio.src = ''; audio = null; }
  if (audioURL) { URL.revokeObjectURL(audioURL); audioURL = null; }
  playback.value = 'stopped';
}
async function playMockAudio() {
  const turn = voiceState.value.turn;
  if (!turn || props.suspended || document.hidden) return;
  stopSpeaking(); const version = playbackEpoch, access = getAccess();
  playback.value = 'loading';
  try {
    const response = await fetch(`/api/voice/turns/${turn.id}/audio`, {
      headers: { Authorization: `Bearer ${access.access_token}`, 'X-Context-Version': String(access.context_version) }, cache: 'no-store',
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) throw new Error('Audio unavailable');
    const blob = await response.blob();
    if (version !== playbackEpoch || access !== getAccess() || disposed || props.suspended || document.hidden) return;
    audioURL = URL.createObjectURL(blob); audio = new Audio(audioURL);
    audio.onended = () => { if (version === playbackEpoch) { stopSpeaking(); playback.value = 'finished'; } };
    audio.onerror = () => { if (version === playbackEpoch) { stopSpeaking(); playback.value = 'failed'; } };
    await audio.play();
    if (version === playbackEpoch) playback.value = 'playing';
  } catch { if (version === playbackEpoch) { stopSpeaking(); playback.value = 'failed'; } }
}
async function retrySpeech() {
  if(busy.value) return;
  busy.value=true; stopSpeaking();
  try { await voice.retrySpeech(); if(voiceState.value.turn?.speech === 'ready') await playMockAudio(); } finally { busy.value=false; }
}
async function endVoice() { stopSpeaking(); await microphone.stop(); return voice.stop(); }
async function startMockVoice() {
  if (props.suspended || pending.value || matchingDraft.value || voiceState.value.support || liveVoice.value && voice.session) return;
  stopSpeaking();
  if (!selected.value) await newConversation();
  if (selected.value && !disposed && !props.suspended) {
    if(liveVoice.value) {
      voice.publish({phase:'permission',error:''});
      try {
        if(!await microphone.start()) return;
        if(disposed || props.suspended || document.hidden) { await microphone.stop(); return; }
      } catch(error) {
        voice.publish({phase:'failed',error:error.name === 'NotAllowedError' ? 'Microphone permission was denied. Type instead.' : error.name === 'NotFoundError' ? 'No microphone was found. Type instead.' : 'Microphone could not start. Type instead.'}); return;
      }
    }
    await voice.start(selected.value,liveVoice.value);
  }
}
async function reviewRecognizedWords() {
  draft.value = voiceState.value.transcript;
  await nextTick(); document.getElementById('chat-message')?.focus();
}
async function editTypedMessage() { await nextTick(); document.getElementById('chat-message')?.focus(); }
function discardDraft() {
  draft.value = ''; crisisNotice.value = '';
  voice.publish({ transcript:'', support:false, submissionEvidence:null });
}
watch(matchingDraft, value => {
  if (value) { crisisNotice.value=CRISIS_NOTICE; endVoice(); }
  else if (!voiceState.value.support && !uncertain.value) crisisNotice.value='';
});
function voiceVisibility() { if (document.hidden) endVoice(); }
watch(() => props.suspended, value => { if (value) endVoice(); });
defineExpose({ endVoice });
onMounted(() => document.addEventListener('visibilitychange', voiceVisibility));
onUnmounted(() => { document.removeEventListener('visibilitychange', voiceVisibility); endVoice(); });
onMounted(async () => { try { configuration.value = await api('/health'); } catch { /* Unknown configuration remains explicit. */ } await loadConversations(); if (!disposed && conversations.value.length) await selectConversation(conversations.value[0].id); });
onUnmounted(() => { disposed = true; epoch++; listEpoch++; clearTimeout(pollTimer); });
</script>

<template>
  <section aria-labelledby="chat-heading" class="chat-view">
    <h1 id="chat-heading">Voice chat</h1>
    <p><strong v-if="configuration?.provider === 'mock'">Mock provider — scripted replies, no live AI.</strong> Use fictional messages only during testing. General wellbeing information and reviewed exercise guidance are the intended scope. This app cannot diagnose, provide treatment or monitor your safety. Crisis support is always available.</p>
    <aside class="support-notice" aria-label="Chat limits and support">
      <p>This coursework chat is not monitored and cannot assess your safety or provide crisis care. Crisis support is available without sending a message. You can stop or leave at any time.</p>
      <button type="button" class="secondary" @click="emit('support', $event)">Open Crisis support</button>
      <p class="small">{{ DETECTION_LIMITS }} Wording checks can flag quotations and negations. They are not clinical assessment or reliable detection; no match establishes safety.</p>
    </aside>
    <section v-if="crisisNotice || matchingDraft || voiceState.support" class="support-notice" aria-label="Review wording and support" role="status">
      <p>{{ CRISIS_NOTICE }}</p>
      <p v-if="voiceState.support && voiceState.submissionEvidence === 'not_saved'">This transcript has not been saved to conversation history or sent for an AI answer. {{ liveVoice ? 'Audio already sent for transcription cannot be recalled.' : 'In this mock preview, no audio was recorded or sent for transcription.' }}</p>
      <p v-else-if="voiceState.support && voiceState.submissionEvidence === 'saved'">Your message remains saved. The generated reply was withheld and was not played.</p>
      <p v-else-if="voiceState.support || uncertain">Submission status is not confirmed. Check saved history before retrying. Stopping cannot recall anything already sent.</p>
      <p v-else>This draft has not been submitted. Existing saved messages are unchanged.</p>
      <div class="voice-actions">
        <button class="secondary" @click="emit('support', $event)">Open Crisis support</button>
        <button v-if="voiceState.support" class="secondary" @click="reviewRecognizedWords">Review recognized words</button>
        <button v-else class="secondary" @click="editTypedMessage">Edit message</button>
        <button class="secondary" :disabled="!!uncertain" @click="discardDraft">Discard draft</button>
        <button class="secondary" @click="endVoice">End conversation</button>
      </div>
    </section>
    <p v-if="storageWarning" role="alert">{{ storageWarning }}</p>
    <section class="voice-controls history-card" aria-labelledby="voice-controls-heading">
      <h2 id="voice-controls-heading">{{ liveVoice ? 'Speak with AI' : 'Voice preview · live access disabled' }}</h2>
      <p v-if="!liveVoice">Transcription is a fixed fictional question. Audio is a short test tone, not spoken AI. Your microphone stays off; nothing is recorded or sent to a provider.</p>
      <p v-if="liveVoice">Start once, then speak. After a short silence your words are sent automatically. Replies use an AI-generated voice. Audio is processed by OpenAI; saved transcripts follow your profile or guest choices.</p>
      <p role="status" v-if="liveVoice">{{ voiceState.phase === 'listening' || voiceState.phase === 'ready' && voice.session ? 'Microphone on · listening' : voiceState.phase === 'processing' ? 'Microphone on · processing; speech is not sent while waiting' : voiceState.phase === 'permission' ? 'Waiting for microphone permission…' : 'Microphone off · ' + voiceState.phase }}</p>
      <p v-else role="status">{{ voiceState.phase === 'listening' ? 'Simulating recognition — microphone off' : voiceState.phase === 'processing' ? 'Preparing the mock reply…' : voiceState.phase === 'connecting' ? 'Saving voice session…' : 'Microphone off · ' + voiceState.phase }}</p>
      <div class="voice-actions">
        <button class="primary" :disabled="pending || suspended || matchingDraft || voiceState.support || liveVoice && !!voice.session" @click="startMockVoice">{{ liveVoice ? 'Start conversation' : 'Run fictional voice demo' }}</button>
        <button class="secondary" :disabled="!voice.session && voiceState.phase !== 'permission'" @click="endVoice">End conversation</button>
      </div>
      <p v-if="voiceState.transcript"><strong>{{ voiceState.support ? 'Recognized words · held for review:' : 'Recognized transcript · automatically submitted:' }}</strong> {{ voiceState.transcript }}</p>
      <p v-if="voiceState.turn">Transcript: {{ voiceState.turn.transcription }} · Message submission: {{ voiceState.turn.submission }} · Audio: {{ voiceState.turn.speech }}</p>
      <button v-if="voiceState.turn?.error_code === 'reply_save_failed'" class="secondary" @click="voice.retrySave()">Retry saving reply</button>
      <button v-if="voiceState.turn?.request?.assistant_persistence === 'saved' && (voiceState.turn.speech === 'failed' || playback === 'failed')" class="secondary" :disabled="busy || suspended || matchingDraft || voiceState.support" @click="retrySpeech">Retry reply audio</button>
      <p v-if="voiceState.error" role="alert">{{ voiceState.error }}</p>
      <label><input type="checkbox" v-model="autoPlay"> Automatically play replies after a voice turn</label>
      <div class="voice-actions">
        <button class="secondary" :disabled="voiceState.turn?.speech !== 'ready' || suspended || matchingDraft || voiceState.support" @click="playMockAudio">{{ liveVoice ? 'Play reply' : 'Play mock audio' }}</button>
        <button class="secondary" :disabled="!['playing', 'loading'].includes(playback)" @click="stopSpeaking">Stop speaking</button>
      </div>
      <p role="status">{{ playback === 'failed' ? 'Audio could not play. The saved text reply is still available.' : playback === 'playing' ? liveVoice ? 'Speaking · AI-generated voice.' : 'Playing mock test tone — not speech.' : playback === 'finished' ? 'Playback finished.' : '' }}</p>
    </section>
    <form v-if="selected" @submit.prevent="submit()" class="chat-form">
      <label for="chat-message">Type instead (fictional message, up to 2,000 characters)</label><textarea id="chat-message" v-model="draft" maxlength="2000" rows="3" :disabled="pending"></textarea>
      <button type="submit" class="primary" :disabled="pending || !draft.trim() || matchingDraft">Send message</button>
      <button v-if="uncertain" type="button" class="secondary" :disabled="busy" @click="submit(true)">Retry submission</button>
      <button v-if="request?.status === 'failed' && !uncertain" type="button" class="secondary" :disabled="busy || !!uncertain" @click="retryReply">Retry reply</button>
    </form>
    <div class="chat-layout">
      <section aria-label="Selected conversation" class="history-card">
        <h2>Current conversation</h2>
        <p v-if="!selected">Create or select a conversation. Practice is available without chatting.</p>
        <p v-if="messageState === 'loading'" role="status">Loading messages…</p>
        <p v-if="messageState === 'failed'" role="alert">Saved messages could not be loaded.</p>
        <p v-if="selected && messageState === 'success' && !messages.length">No messages yet.</p>
        <p v-if="notice" role="status">{{ notice }}</p>
        <ol class="request-list">
          <li v-for="group in messageGroups" :key="group.id">
            <ol class="message-list"><li v-for="message in group.messages" :key="message.id"><strong>{{ message.role === 'user' ? 'You (fictional input)' : `Assistant (${message.provider})` }}</strong><p class="message-content">{{ displayedMessage(message) }}</p><small>{{ new Date(message.created_at).toLocaleString() }} · Order {{ message.sequence }} · Saved · Request {{ message.request_status }}</small></li></ol>
            <template v-if="request?.id === group.id">
        <p v-if="request?.status === 'pending'" role="status">Message saved. Waiting for the reply…</p>
        <p v-if="request?.status === 'succeeded' && !uncertain && !crisisNotice && !matchingDraft" role="status">{{ request.provider }} reply saved. Retrieval: {{ request.retrieval_outcome }}. Provider calls across attempts: {{ request.provider_call_count }}.</p>
        <p v-if="request?.failure_stage && !uncertain" class="small">Failure stage: {{ request.failure_stage }}. Provider calls across attempts: {{ request.provider_call_count }}.</p>
        <p v-if="request?.status === 'failed' && !uncertain" role="alert">{{ errorText }}</p>
        <button v-if="request && !uncertain" class="secondary" :disabled="busy" @click="poll(request.id, epoch)">Check request status</button>
            </template>
          </li>
        </ol>



      </section>
      <section aria-label="Conversation history" class="history-card">
        <h2>Conversation history</h2>
        <button class="primary" :disabled="busy" @click="newConversation">New conversation</button>
        <button class="secondary" :disabled="listState === 'loading'" @click="loadConversations()">Refresh conversations</button>
        <p v-if="listState === 'loading'" role="status">Loading conversations…</p>
        <p v-if="listState === 'failed'" role="alert">Could not load conversations. Previously displayed items may be out of date.</p>
        <p v-if="listState === 'success' && !conversations.length">No saved conversations yet.</p>
        <ul class="conversation-list"><li v-for="item in conversations" :key="item.id"><button class="secondary" :aria-current="selected === item.id ? 'true' : undefined" @click="selectConversation(item.id)">{{ new Date(item.created_at).toLocaleString() }}<code>{{ item.id }}</code></button></li></ul>
        <button v-if="conversationCursor !== null" class="secondary" :disabled="listState === 'loading'" @click="loadConversations(true)">More conversations</button>
      </section>
    </div>
  </section>
</template>

<style scoped>
.support-notice{border:1px solid #768972;border-radius:8px;padding:16px;margin:16px 0;max-width:65ch}.support-notice p{margin:8px 0}.chat-layout{display:grid;gap:20px}.chat-view>p{max-width:65ch}.conversation-list,.message-list,.request-list{list-style:none;padding:0}.conversation-list li{margin-top:10px}.conversation-list button{width:100%;text-align:left}.conversation-list button[aria-current=true]{border:2px solid #335743}code{display:block;overflow-wrap:anywhere;font-size:11px;color:#526456}.message-list li{border-bottom:1px solid #dce2d4;padding:16px 0}.message-content{white-space:pre-wrap;overflow-wrap:anywhere;margin:8px 0}.message-list small{display:block}.chat-form{display:grid;gap:10px;margin:20px 0}.chat-form textarea,.chat-form select{font:inherit;padding:10px;border:1px solid #768972;border-radius:6px;background:#fffefa;color:#263d36;max-width:100%}.chat-form textarea:focus-visible{outline:3px solid #9d4c27;outline-offset:3px}.history-card>button{margin:4px}.chat-form button{justify-self:start}
</style>

<style scoped>
.voice-controls { margin-block: 20px; } .voice-actions { display:flex; gap:12px; flex-wrap:wrap; margin-block:12px; } .voice-controls p { overflow-wrap:anywhere; } .voice-controls button { min-height:44px; } @media(min-width:1000px) { .chat-layout { grid-template-columns:minmax(0,2fr) minmax(220px,1fr); align-items:start; } } @media(max-width:480px) { .voice-actions button { flex:1 1 150px; } .voice-controls { padding:16px; } }
</style>
