<script setup>
import { onMounted, ref } from 'vue';
import App from './App.vue';
import SupportContent from './components/SupportContent.vue';
import { api } from './api.js';
import { getAccess, setAccess } from './identityAccess.js';
const identity = ref(null), chooser = ref(true), profiles = ref([]), busy = ref(false), error = ref(''), support = ref(false);
const name = ref(''), age = ref(''), gender = ref(''), disposition = ref(''), exitConfirm = ref(false);
const pending = ref(null);
function apply(result) {
  const previous = identity.value;
  const value = { ...getAccess(), ...result };
  setAccess(value); identity.value = value; chooser.value = value.mode === 'chooser';
  if (previous?.mode === 'guest' && previous.active_owner_id !== value.active_owner_id) {
    for (const key of Object.keys(localStorage)) if (key.startsWith(`coursework-session-outbox:${previous.active_owner_id}:`)) localStorage.removeItem(key);
    for (const key of Object.keys(sessionStorage)) if (key.startsWith(previous.active_owner_id + ':')) sessionStorage.removeItem(key);
  }
}
async function listing() { profiles.value = (await api('/profiles')).profiles; }
async function boot() {
  busy.value = true; error.value = '';
  try {
    if (!getAccess()?.access_token) apply(await api('/identity/bootstrap', 'POST', { bootstrap_id: crypto.randomUUID() }));
    else apply(await api('/identity'));
    await listing();
  } catch (e) { error.value = e.message; }
  finally { busy.value = false; }
}
async function perform(path, body) {
  if (busy.value) return;
  pending.value = { path, body }; busy.value = true; error.value = '';
  try {
    const result = await api(path, 'POST', body);
    if (result.profile) { await listing(); name.value = ''; age.value = ''; gender.value = ''; }
    else { apply(result); exitConfirm.value = false; disposition.value = ''; }
    pending.value = null;
  } catch (e) { error.value = e.message; }
  finally { busy.value = false; }
}
const action = () => ({ operation_id: crypto.randomUUID(), expected_context_version: identity.value.context_version });
async function choose() { chooser.value = true; error.value = ''; disposition.value = ''; try { await listing(); } catch (e) { error.value = e.message; } }
function select(id) {
  if (identity.value.mode === 'guest' && !disposition.value) { error.value = 'Choose whether to save or discard guest activity first.'; return; }
  perform('/identity/select', { ...action(), profile_id: id, guest_disposition: identity.value.mode === 'guest' ? disposition.value : null });
}
function leave() {
  if (identity.value.mode === 'guest') { exitConfirm.value = true; return; }
  perform('/identity/leave', action());
}
function create() { if (pending.value) { error.value = 'Retry the pending operation before creating another profile.'; return; } perform('/profiles', { operation_id: crypto.randomUUID(), profile_id: crypto.randomUUID(), display_name: name.value, age: age.value === '' ? null : Number(age.value), gender: gender.value || null }); }
onMounted(boot);
</script>
<template>
  <App v-if="identity?.active_owner_id" v-show="!chooser" :key="identity.active_owner_id + ':' + identity.context_version" :identity="identity" @choose="choose" @leave="leave" @delete="revision => perform('/profile/delete', { ...action(), expected_revision: revision, confirm_delete: true })" @updated="display_name => identity.display_name = display_name" />
  <main v-if="chooser" class="shell profile-gate">
    <section class="history-card" role="dialog" aria-labelledby="chooser-title">
      <div class="panel-heading"><h1 id="chooser-title">A little space for you</h1><button class="support-link" @click="support = !support">Crisis support</button></div>
      <SupportContent v-if="support" />
      <p>Use fictional details only. Local profiles have no password and are not secure authentication.</p>
      <button v-if="identity?.mode === 'chooser'" class="primary" :disabled="busy" @click="perform('/identity/guest', action())">Continue as guest</button>
      <button v-else-if="identity?.active_owner_id" class="primary" @click="chooser = false">Continue {{ identity.mode === 'guest' ? 'as guest' : 'with ' + identity.display_name }}</button>
      <fieldset v-if="identity?.mode === 'guest'"><legend>Before switching to a profile</legend><label><input type="radio" v-model="disposition" value="save"> Save this guest activity to my profile</label><label><input type="radio" v-model="disposition" value="discard"> Discard guest activity when I select a profile</label></fieldset>
      <p v-if="!profiles.length && !busy">No saved profiles yet. Guest access needs no personal information.</p>
      <ul class="profile-list"><li v-for="profile in profiles" :key="profile.id"><button class="secondary" :disabled="busy" @click="select(profile.id)">{{ profile.display_name }} <small>Created {{ new Date(profile.created_at).toLocaleString() }}</small></button></li></ul>
      <details><summary>Create a profile</summary><form class="profile-form" @submit.prevent="create"><label>Display name <input v-model="name" required maxlength="60"></label><label>Age (optional) <input v-model="age" type="number" min="0" max="120" step="1"></label><label>Gender (optional) <input v-model="gender" maxlength="60"></label><button class="secondary" :disabled="busy || !identity">Save profile</button><p class="small">After saving, select your profile above. Age and gender can be skipped.</p></form></details>
      <button v-if="!identity && !busy" class="secondary" @click="boot">Retry connection</button>
    </section>
  </main>
  <section v-if="exitConfirm" class="identity-notice" role="dialog" aria-label="Confirm Exit guest"><p>Exit guest and permanently discard this guest activity?</p><button class="stop" :disabled="busy" @click="perform('/identity/leave', { ...action(), confirm_discard: true })">Exit guest and discard</button><button class="secondary" @click="exitConfirm = false">Cancel</button></section>
  <aside v-if="busy || error" class="identity-notice" aria-live="polite"><p v-if="busy">Saving or loading profile…</p><p v-if="error" role="alert">{{ error }}</p><button v-if="pending && !busy" class="secondary" @click="perform(pending.path, pending.body)">Retry same operation</button></aside>
</template>
