<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { api } from '../api.js';
const month = ref(new Date().toLocaleDateString('sv-SE').slice(0, 7));
const zone = ref(Intl.DateTimeFormat().resolvedOptions().timeZone);
const events = ref([]), state = ref('loading'), error = ref('');
let generation = 0;
const days = computed(() => {
  const groups = new Map();
  for (const event of events.value) {
    if (!groups.has(event.local_date)) groups.set(event.local_date, []);
    groups.get(event.local_date).push(event);
  }
  return [...groups];
});
const dayLabel = day => new Date(day + 'T12:00:00Z').toLocaleDateString(undefined, { timeZone: 'UTC', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const timeLabel = event => new Date(event.completed_at).toLocaleTimeString(undefined, { timeZone: zone.value, hour: 'numeric', minute: '2-digit', second: '2-digit', timeZoneName: 'short' });
async function load() {
  const current = ++generation;
  zone.value = Intl.DateTimeFormat().resolvedOptions().timeZone;
  state.value = 'loading'; events.value = []; error.value = '';
  try {
    let cursor = 0, result = [];
    do {
      const page = await api(`/calendar?month=${month.value}&timezone=${encodeURIComponent(zone.value)}&cursor=${cursor}`);
      if (current !== generation) return;
      result.push(...page.events); cursor = page.next_cursor;
    } while (cursor !== null);
    events.value = result; state.value = 'success';
  } catch (e) { if (current === generation) { state.value = 'failed'; error.value = e.message; } }
}
function move(amount) {
  const [year, number] = month.value.split('-').map(Number);
  const date = new Date(Date.UTC(year, number - 1 + amount, 1));
  const next = date.toISOString().slice(0, 7);
  if (next < '1900-01' || next > '2100-12') return;
  month.value = next; load();
}
function checkZone() { if (zone.value !== Intl.DateTimeFormat().resolvedOptions().timeZone) load(); }
onMounted(() => { load(); window.addEventListener('focus', checkZone); });
onUnmounted(() => { generation++; window.removeEventListener('focus', checkZone); });
</script>
<template>
  <section class="history-card calendar-view" aria-labelledby="calendar-heading">
    <h1 id="calendar-heading">Exercise calendar</h1>
    <p>Completed practices, shown on the day they finished.</p>
    <p class="small">Timezone: {{ zone }}</p>
    <div class="calendar-controls">
      <button class="secondary" aria-label="Previous month" :disabled="month === '1900-01'" @click="move(-1)">← Previous</button>
      <label>Month <input type="month" min="1900-01" max="2100-12" v-model="month" @change="month && load()"></label>
      <button class="secondary" aria-label="Next month" :disabled="month === '2100-12'" @click="move(1)">Next →</button>
      <button class="secondary" :disabled="state === 'loading'" @click="load">Refresh calendar</button>
    </div>
    <p v-if="state === 'loading'" role="status">Loading completed practices…</p>
    <p v-if="state === 'failed'" role="alert">Calendar could not load. {{ error }} Use Refresh calendar to retry.</p>
    <p v-if="state === 'success' && !events.length" role="status">No completed practices this month.</p>
    <ol class="calendar-days" aria-label="Completed practices by day">
      <li v-for="[day, entries] in days" :key="day">
        <h2>{{ dayLabel(day) }}</h2>
        <ul><li v-for="event in entries" :key="event.session_id" :data-session-id="event.session_id">
          <strong>{{ event.exercise_name }}</strong><br>
          <time :datetime="event.completed_at">{{ timeLabel(event) }}</time>
          <span v-if="event.is_fixture"> · Fictional fixture</span>
        </li></ul>
      </li>
    </ol>
    <p class="small muted">Stopped and interrupted practices remain in Session history.</p>
  </section>
</template>
