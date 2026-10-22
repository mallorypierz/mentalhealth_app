<script setup>
import { computed, ref, onMounted, onUnmounted, nextTick } from 'vue';
import { Exercise, LatestRequest } from './exercise.js';
import { api } from './api.js';
import ChatView from './components/ChatView.vue';
import { SessionPersistence } from './sessionPersistence.js';
const engine = new Exercise();
const exercise = ref(engine.snapshot());
const view = ref('practice');
const support = ref(false);
const practiceScreen = ref(null), fullscreenButton = ref(null), fullscreen = ref(false);
const fullscreenNotice = ref('');
let nativeFullscreen = false;
async function minimizePractice() {
  if (document.fullscreenElement === practiceScreen.value) await document.exitFullscreen();
  fullscreen.value = false; nativeFullscreen = false; fullscreenNotice.value = '';
  await nextTick(); fullscreenButton.value?.focus();
}
async function toggleFullscreen() {
  if (fullscreen.value) return minimizePractice();
  fullscreen.value = true;
  await nextTick();
  try {
    if (!practiceScreen.value.requestFullscreen) throw new Error('unsupported');
    await practiceScreen.value.requestFullscreen(); nativeFullscreen = true;
  } catch {
    fullscreenNotice.value = 'Expanded to fill this window. Browser fullscreen is unavailable.';
  }
  fullscreenButton.value?.focus();
}
function fullscreenChanged() {
  if (nativeFullscreen && !document.fullscreenElement) {
    fullscreen.value = false; nativeFullscreen = false; fullscreenNotice.value = '';
    nextTick(() => fullscreenButton.value?.focus());
  }
}
function fullscreenKey(event) {
  if (event.key === 'Escape' && fullscreen.value) { event.preventDefault(); minimizePractice(); }
}
const supportHeading = ref(null);
let supportTrigger;
const reduceMotion = ref(matchMedia('(prefers-reduced-motion: reduce)').matches);
const active = computed(() => ['running', 'paused'].includes(exercise.value.state));
const cueScale = computed(() => {
  if (!active.value || reduceMotion.value) return 1;
  const within = exercise.value.elapsed % 10000;
  // Ease for 250ms on each side of a phase boundary (500ms total).
  // Derive scale from the exercise clock so pause/resume cannot add visual lag.
  const easedProgress = (elapsed, duration) => {
    const ramp = 250;
    if (elapsed < ramp) return elapsed * elapsed / (2 * ramp * (duration - ramp));
    if (elapsed > duration - ramp) return 1 - (duration - elapsed) ** 2 / (2 * ramp * (duration - ramp));
    return (elapsed - ramp / 2) / (duration - ramp);
  };
  return within < 4000
    ? 0.85 + 0.15 * easedProgress(within, 4000)
    : 1 - 0.15 * easedProgress(within - 4000, 6000);
});
const finished = computed(() => ['stopped', 'completed'].includes(exercise.value.state));
const history = ref([]), historyState = ref('idle'), nextCursor = ref(null);
const saveStates = ref({});
const persistence = new SessionPersistence(update => { saveStates.value = { ...saveStates.value, [update.id]: update }; });
const historyRequests = new LatestRequest();
async function loadHistory(more = false) {
  const cursor = more ? nextCursor.value : 0;
  if (cursor === null) return;
  historyState.value = 'loading';
  await historyRequests.run(() => api(`/sessions?cursor=${cursor}&limit=20`), ({ value, error }) => {
    if (error) { historyState.value = 'failed'; return; }
    history.value = more ? [...history.value, ...value.sessions] : value.sessions;
    nextCursor.value = value.next_cursor; historyState.value = 'success';
  });
}
let sessionId, started, recorded = false, timer, checkpointTimer;
const currentSave = computed(() => saveStates.value[sessionId]);
const unresolved = computed(() => Object.values(saveStates.value).filter(item => ['failed', 'unknown'].includes(item.state)));
const hiddenPause = ref(false);
function checkpoint(ended = null) { persistence.checkpoint(sessionId, engine.snapshot(), ended); }
function visibilityChanged() {
  if (document.hidden && engine.state === 'running') { hiddenPause.value = true; pause(); }
}
onMounted(async () => { document.addEventListener('visibilitychange', visibilityChanged); document.addEventListener('fullscreenchange', fullscreenChanged); document.addEventListener('keydown', fullscreenKey); await persistence.recover(); });
const heading = ref(null);
const focusHeading = () => nextTick(() => heading.value?.focus());
function sync() {
  exercise.value = engine.snapshot();
  if (finished.value && !recorded) {
    recorded = true; clearInterval(timer); clearInterval(checkpointTimer);
    checkpoint(new Date().toISOString()); focusHeading();
  }
}
function start() {
  clearInterval(timer); clearInterval(checkpointTimer); recorded = false; hiddenPause.value = false;
  sessionId = crypto.randomUUID(); started = new Date().toISOString();
  persistence.begin(sessionId, started);
  engine.start(); sync(); view.value = 'practice';
  timer = setInterval(() => { engine.tick(); sync(); }, 50);
  checkpointTimer = setInterval(() => { if (active.value) checkpoint(); }, 5000); focusHeading();
}
function pause() { engine.pause(); sync(); if (active.value) checkpoint(); }
function resume() { if (!support.value) { hiddenPause.value = false; engine.resume(); sync(); if (active.value) checkpoint(); } }
function stop() { engine.stop(); sync(); }
async function openSupport(event) {
  supportTrigger = event.currentTarget;
  if (active.value) pause();
  support.value = true; await nextTick(); supportHeading.value?.focus();
}
async function closeSupport() { support.value = false; await nextTick(); supportTrigger?.focus(); }
function navigate(destination) { if (fullscreen.value) minimizePractice(); view.value = destination; if (destination === 'history') loadHistory(); focusHeading(); }
onUnmounted(() => { clearInterval(timer); clearInterval(checkpointTimer); historyRequests.cancel(); document.removeEventListener('visibilitychange', visibilityChanged); document.removeEventListener('fullscreenchange', fullscreenChanged); document.removeEventListener('keydown', fullscreenKey); });
</script>

<template>
  <div class="shell">
    <header class="topbar" :inert="fullscreen">
      <a class="brand" href="#main" aria-label="A little space, skip to main content"><span class="brand-mark" aria-hidden="true">◒</span> a little space<span class="brand-dot">.</span></a>
      <span class="demo-tag">COURSEWORK DEMO</span>
    </header>
    <div class="workspace">
      <aside class="sidebar" aria-label="Prototype navigation" :inert="fullscreen">
        <p class="eyebrow">YOUR SPACE</p>
        <nav aria-label="Main navigation">
          <button :class="{ selected: view === 'practice' }" @click="navigate('practice')" :aria-current="view === 'practice' ? 'page' : undefined"><span aria-hidden="true">◉</span> Practice</button>
          <button :disabled="active" :class="{ selected: view === 'history' }" @click="navigate('history')" :aria-current="view === 'history' ? 'page' : undefined"><span aria-hidden="true">≡</span> Session history</button>
          <button :disabled="active" :class="{ selected: view === 'chat' }" @click="navigate('chat')" :aria-current="view === 'chat' ? 'page' : undefined">Optional chat</button>
        </nav>
        <p v-if="active" class="small muted">History is available after stopping or completing.</p>
        <div class="sidebar-note"><span class="tiny-line"></span><p>A moment of practice.<br>At your own pace.</p><p class="small muted">A fictional coursework experience, not therapy or a monitored service.</p></div>
      </aside>
      <main id="main" ref="practiceScreen" :class="{ 'practice-fullscreen': fullscreen }" tabindex="-1">
        <div class="page-top"><button v-if="fullscreen" class="secondary fullscreen-icon" aria-label="Minimize" title="Minimize" @click="minimizePractice"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 4l6 6M4 10h6V4M20 20l-6-6M14 20v-6h6" /></svg></button><span class="eyebrow">{{ view === 'history' ? 'YOUR RECORDS' : view === 'chat' ? 'OPTIONAL CHAT' : 'A MOMENT TO PRACTICE' }}</span><button class="support-link" @click="openSupport">Crisis support <span aria-hidden="true">↗</span></button></div>
        <section v-if="support" class="support-panel" aria-labelledby="support-title" @keydown.esc="closeSupport">
          <div class="panel-heading"><h2 id="support-title" ref="supportHeading" tabindex="-1">Crisis support</h2><button class="secondary" @click="closeSupport">Close support</button></div>
          <p v-if="active">Practice is paused. Closing this panel will not resume it. Use Resume when you choose.</p>
          <p>This demo is not monitored. The following resource serves the United States and its territories.</p>
          <p><strong>988 Suicide &amp; Crisis Lifeline</strong></p>
          <div class="support-actions"><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Online chat ↗</a></div>
          <p class="small">Resource checked through the helpline lookup on October 22, 2026. Availability was not tested by contacting the service.</p>
          <button v-if="active" class="stop" @click="stop">Stop practice</button>
        </section>
        <template v-if="view === 'practice'">
          <div class="title-block"><h1 ref="heading" tabindex="-1">{{ active ? 'One breath at a time.' : finished ? (exercise.state === 'completed' ? 'Practice completed.' : 'Practice stopped.') : 'Make a little space.' }}</h1><p>{{ active ? 'Follow the cue. Pause or stop whenever you choose.' : finished ? 'You choose what comes next.' : 'A short breathing practice, with room to go at your own pace.' }}</p></div>
          <p v-if="hiddenPause" role="status">Practice paused when this tab was hidden. Resume when you choose.</p>
          <p v-if="fullscreenNotice" role="status">{{ fullscreenNotice }}</p>
          <section class="practice-card" aria-label="Breathing practice">
            <div class="fullscreen-control"><button ref="fullscreenButton" class="secondary fullscreen-icon" :aria-expanded="fullscreen" :aria-label="fullscreen ? 'Minimize' : 'Full screen'" :title="fullscreen ? 'Minimize' : 'Full screen'" @click="toggleFullscreen"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path :d="fullscreen ? 'M4 4l6 6M4 10h6V4M20 20l-6-6M14 20v-6h6' : 'M10 10 4 4M4 10V4h6M14 14l6 6M14 20h6v-6'" /></svg></button></div>
            <div class="card-meta"><span class="pill">{{ active ? 'IN PRACTICE' : finished ? 'SESSION RESULT' : 'PACED BREATHING' }}</span><span class="small muted">{{ active ? `Cycle ${exercise.cycle} of 6` : '60 seconds · 6 cycles' }}</span></div>
            <div class="practice-body">
              <div class="orb-wrap" aria-hidden="true"><div class="orb" :style="{ transform: `scale(${cueScale})` }" :class="{ moving: active && !reduceMotion, paused: exercise.state === 'paused', inhale: exercise.phase === 'Breathe in' }"><div class="orb-inner"><span>{{ active ? (exercise.state === 'paused' ? 'Ⅱ' : exercise.count) : finished ? '✓' : '4 / 6' }}</span><small>{{ active ? (exercise.state === 'paused' ? 'paused' : 'seconds') : finished ? exercise.state : 'in · out' }}</small></div></div></div>
              <div class="practice-copy">
                <template v-if="!active && !finished"><h2>60-second breathing practice</h2><p>Breathe in for four seconds.<br>Breathe out for six.<br>We’ll guide you through six cycles.</p><button class="primary" :disabled="support" @click="start">Start practice <span aria-hidden="true">→</span></button><p class="small muted">No check-in or typing needed.</p></template>
                <template v-else-if="active"><p v-if="exercise.state === 'paused'" class="eyebrow">TAKE YOUR TIME</p><h2 role="status">{{ exercise.state === 'paused' ? 'Paused' : exercise.phase }}</h2><p class="counter-text"><template v-if="exercise.state === 'paused'">Resume only when you choose.</template><template v-else><span class="phase-count-sr">{{ exercise.count }} seconds in this phase. </span>{{ exercise.remaining }} seconds remaining</template></p><div class="exercise-actions"><button v-if="exercise.state === 'running'" class="primary" @click="pause">Pause</button><button v-else class="primary" :disabled="support" @click="resume">Resume</button><button class="stop" @click="stop">Stop practice</button></div><p v-if="support" class="small">Close support to enable Resume.</p></template>
                <template v-else><h2>{{ exercise.state === 'completed' ? 'Six cycles completed.' : 'Stopped, on your terms.' }}</h2><p>{{ Math.floor(exercise.elapsed / 1000) }} seconds of active practice.<br>{{ currentSave?.message || 'Save not yet confirmed.' }}</p><div class="exercise-actions"><button class="primary" :disabled="support" @click="start">Practice again</button><button class="secondary" @click="navigate('history')">View history</button></div></template>
              </div>
            </div>
            <div v-if="active" class="progress-track" role="progressbar" aria-label="Practice progress" :aria-valuenow="Math.floor(exercise.elapsed / 1000)" :aria-valuemax="60" aria-valuemin="0"><div :style="{ width: `${exercise.elapsed / 600}%` }"></div></div>
            <div class="card-bottom"><label class="motion-control"><input type="checkbox" v-model="reduceMotion"> Use a still cue</label><span class="small muted">{{ reduceMotion ? 'Text + countdown. No animation.' : 'Gentle motion + countdown' }}</span></div>
            <p v-if="currentSave" role="status" class="save-status" :class="{ 'save-status-error': ['failed', 'unknown'].includes(currentSave.state) }">{{ currentSave.message }}</p>
          </section>
          <section v-if="unresolved.length" aria-label="Unsaved sessions" class="intro-card"><h2>Sessions needing attention</h2><p>These local outcomes are separate from saved history.</p><div v-for="item in unresolved" :key="item.id"><p>{{ item.message }} <code>{{ item.id }}</code></p><button class="secondary" @click="persistence.retry(item.id)">Retry save</button></div></section>

        </template>
        <ChatView v-else-if="view === 'chat'" @support="openSupport" />
        <template v-else><div class="title-block"><h1 ref="heading" tabindex="-1">Your practice, recorded.</h1><p>Duration and status only. These records don’t measure wellbeing.</p></div><section class="history-card"><div class="panel-heading"><h2>Session history</h2><span class="pill">SAVED FICTIONAL RECORDS</span></div><p v-if="historyState === 'loading'" role="status">Loading saved history…</p><p v-if="historyState === 'failed'" role="alert">Could not load saved history. Previously displayed rows may be out of date.</p><p v-if="historyState === 'success' && !history.length">No saved sessions yet.</p><button class="secondary" :disabled="historyState === 'loading'" @click="loadHistory()">Refresh history</button><div class="table-scroll"><table><caption class="small muted">SQLite-backed records for one fictional coursework profile. Interrupted duration is the last confirmed checkpoint.</caption><thead><tr><th scope="col">Session</th><th scope="col">Duration</th><th scope="col">Status</th></tr></thead><tbody><tr v-for="row in history" :key="row.id"><td>{{ new Date(row.started_at).toLocaleString() }}<small>{{ row.is_fixture ? 'Fictional fixture' : 'Breathing session · saved' }}</small></td><td>{{ Math.floor(row.active_duration_ms / 1000) }}s</td><td><span class="status-chip">{{ row.status }}</span></td></tr></tbody></table></div><button v-if="nextCursor !== null" class="secondary" :disabled="historyState === 'loading'" @click="loadHistory(true)">Load more</button><button class="secondary" @click="navigate('practice')">Back to practice</button></section></template>
      </main>
    </div>
  </div>
</template>

<style scoped>
.phase-count-sr { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip-path:inset(50%); white-space:nowrap; border:0; }
.save-status { margin:0; padding:0 20px 14px; font-size:11px; line-height:1.5; color:#59675e; overflow-wrap:anywhere; }
.save-status code { font-size:inherit; }
.save-status-error { font-size:13px; color:#813d28; }
.fullscreen-icon { display:inline-flex; align-items:center; justify-content:center; min-width:44px; min-height:44px; padding:10px; }
.fullscreen-icon svg { width:24px; height:24px; fill:none; stroke:currentColor; stroke-width:2.5; stroke-linecap:round; stroke-linejoin:round; }
.fullscreen-control { display:flex; justify-content:flex-end; padding:16px 20px 0; }
main.practice-fullscreen { position:fixed; inset:0; z-index:100; width:100%; height:100dvh; max-width:none; margin:0; padding:20px; overflow:auto; box-sizing:border-box; background:#f6f5f0; }
.practice-fullscreen .page-top { position:sticky; top:-20px; z-index:2; background:#f6f5f0; padding:12px 0; display:flex; flex-wrap:wrap; gap:12px; }
.practice-fullscreen .title-block, .practice-fullscreen footer { display:none; }
.practice-fullscreen .practice-card { max-width:1100px; margin:0 auto; }
.practice-fullscreen .support-panel { position:relative; z-index:3; }
@media (max-width:600px) { main.practice-fullscreen { padding:12px; } .practice-fullscreen .page-top { top:-12px; } }
</style>
