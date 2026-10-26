<script setup>
import { onMounted, ref } from 'vue';
import { api } from '../api.js';
const props = defineProps(['identity']);
const emit = defineEmits(['choose', 'leave', 'delete', 'updated']);
const profile = ref(null), state = ref('loading'), error = ref(''), deletion = ref(false);
async function load() {
  if (props.identity.mode === 'guest') { state.value = 'success'; return; }
  state.value = 'loading';
  try { profile.value = (await api('/profile')).profile; state.value = 'success'; }
  catch (e) { state.value = 'failed'; error.value = e.message; }
}
async function save() {
  state.value = 'saving';
  try {
    const p = profile.value;
    profile.value = (await api('/profile', 'PATCH', { operation_id: crypto.randomUUID(), expected_revision: p.revision, display_name: p.display_name, age: p.age === '' ? null : p.age, gender: p.gender || null })).profile;
    state.value = 'saved'; emit('updated', profile.value.display_name);
  } catch (e) { state.value = 'failed'; error.value = e.message; }
}
onMounted(load);
</script>
<template>
<section class="history-card">
  <h1>{{ identity.mode === 'guest' ? 'Guest activity' : 'Your profile' }}</h1>
  <p>Local fictional profiles. This chooser is not secure sign-in; anyone using this app can select a profile.</p>
  <p v-if="state === 'loading'" role="status">Loading profile…</p>
  <p v-if="state === 'saving'" role="status">Saving…</p>
  <p v-if="state === 'saved'" role="status">Profile saved.</p>
  <p v-if="state === 'failed'" role="alert">{{ error }} <button class="secondary" @click="load">Reload profile</button></p>
  <form v-if="profile" class="profile-form" @submit.prevent="save">
    <label>Display name <input v-model="profile.display_name" required maxlength="60"></label>
    <label>Age (optional) <input v-model.number="profile.age" type="number" min="0" max="120" step="1"></label>
    <label>Gender (optional) <input v-model="profile.gender" maxlength="60"></label>
    <button class="primary" :disabled="state === 'saving'">Save profile</button>
    <p class="small">Saved since {{ new Date(profile.created_at).toLocaleDateString() }}. View saved practices in Session history or Calendar, and saved messages in Optional chat.</p>
  </form>
  <p v-if="identity.mode === 'guest'">Guest activity stays through refresh and navigation. Exit guest or a confirmed discard removes it. You may explicitly save it to a profile.</p>
  <div class="exercise-actions">
    <button class="secondary" @click="emit('choose')">{{ identity.mode === 'guest' ? 'Save this guest activity to my profile' : 'Switch profile' }}</button>
    <button class="secondary" @click="emit('leave')">{{ identity.mode === 'guest' ? 'Exit guest' : 'Leave profile' }}</button>
    <button v-if="profile" class="stop" @click="deletion = true">Delete profile and its saved activity</button>
  </div>
  <div v-if="deletion" role="group" aria-label="Confirm deletion"><p>Delete this profile and all its saved activity? This cannot be undone.</p><button class="stop" @click="emit('delete', profile.revision)">Confirm deletion</button><button class="secondary" @click="deletion = false">Cancel</button></div>
</section>
</template>
