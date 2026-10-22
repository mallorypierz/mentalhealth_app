<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { api } from '../api.js';
import { matchesCrisisPhrase, CRISIS_NOTICE } from '../crisis.js';
function displayedMessage(message) {
  if (message.role !== 'assistant' || message.provider !== 'mock') return message.content;
  // Presentation only: retain the original reply and citation in the API/database.
  return message.content.replace(/Record \[[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\]\. ?/gi, '');
}
const emit = defineEmits(['support']);
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
const uncertain = ref(null), storageWarning = ref('');
let epoch = 0, pollTimer, disposed = false, listEpoch = 0;
const pending = computed(() => busy.value || request.value?.status === 'pending' || !!uncertain.value);
const errorText = computed(() => ({
  support_notice: 'No AI call was made for this attempt. Your previously saved message remains in history. Crisis support is available.',
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
  invalid_provider_output: 'The provider returned an invalid response. No assistant reply was saved.',
}[request.value?.error_code] || 'Request failed. No assistant reply is saved.'));
const journalKey = id => `coursework-chat-pending:${id}`;
function readJournal(id) { try { return JSON.parse(sessionStorage.getItem(journalKey(id)) || 'null'); } catch { return null; } }
function writeJournal(id, body) {
  try { if (body) sessionStorage.setItem(journalKey(id), JSON.stringify(body)); else sessionStorage.removeItem(journalKey(id)); }
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
  const version = ++epoch; clearTimeout(pollTimer);
  crisisNotice.value = '';
  selected.value = id; messages.value = []; messageCursor.value = null; request.value = null;
  messageState.value = 'loading'; notice.value = ''; busy.value = false;
  uncertain.value = readJournal(id); draft.value = uncertain.value?.content || '';
  await refreshMessages(version);
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
onMounted(async () => { try { configuration.value = await api('/health'); } catch { /* Unknown configuration remains explicit. */ } await loadConversations(); if (!disposed && conversations.value.length) await selectConversation(conversations.value[0].id); });
onUnmounted(() => { disposed = true; epoch++; listEpoch++; clearTimeout(pollTimer); });
</script>

<template>
  <section aria-labelledby="chat-heading" class="chat-view">
    <h1 id="chat-heading">Optional chat</h1>
    <p><strong v-if="configuration?.provider === 'mock'">Mock provider — scripted replies, no live AI.</strong> Use fictional messages only. This coursework demo is not therapy or a monitored service.</p>
    <aside class="support-notice" aria-label="Chat limits and support">
      <p>This coursework chat is not monitored and cannot assess your safety or provide crisis care. Crisis support is available without sending a message. You can stop or leave at any time.</p>
      <button type="button" class="secondary" @click="emit('support', $event)">Open Crisis support</button>
      <p class="small">A limited phrase rule can miss wording or flag quotations and negations. It is not clinical assessment or reliable crisis detection. A message that does not match is not evidence of safety.</p>
    </aside>
    <p v-if="crisisNotice || matchingDraft" role="status">{{ matchingDraft && !uncertain ? CRISIS_NOTICE : crisisNotice }}</p>
    <p v-if="storageWarning" role="alert">{{ storageWarning }}</p>
    <form v-if="selected" @submit.prevent="submit()" class="chat-form">
      <label for="chat-message">Fictional message (up to 2,000 characters)</label><textarea id="chat-message" v-model="draft" maxlength="2000" rows="3" :disabled="pending"></textarea>
      <button type="submit" class="primary" :disabled="pending || !draft.trim()">Send message</button>
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
