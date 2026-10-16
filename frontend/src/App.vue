<script setup>
import { computed, ref, onUnmounted, nextTick } from 'vue';
import { Exercise, LatestRequest } from './exercise.js';
const engine = new Exercise();
const exercise = ref(engine.snapshot());
const view = ref('practice');
const support = ref(false);
const supportHeading = ref(null);
let supportTrigger;
const reduceMotion = ref(matchMedia('(prefers-reduced-motion: reduce)').matches);
const active = computed(() => ['running', 'paused'].includes(exercise.value.state));
const cueScale = computed(() => {
  if (!active.value || reduceMotion.value) return 1;
  const within = exercise.value.elapsed % 10000;
  return within < 4000 ? 0.85 + 0.15 * within / 4000 : 1 - 0.15 * (within - 4000) / 6000;
});
const finished = computed(() => ['stopped', 'completed'].includes(exercise.value.state));
const history = ref([{ id: 'fixture-001', started: 'Fictional example', duration: 60, status: 'completed', fixture: true }]);
let sessionId, started, recorded = false, timer;
const heading = ref(null);
const focusHeading = () => nextTick(() => heading.value?.focus());
function sync() {
  exercise.value = engine.snapshot();
  if (finished.value && !recorded) {
    history.value.unshift({ id: sessionId, started, duration: Math.floor(exercise.value.elapsed / 1000), status: exercise.value.state, fixture: false });
    recorded = true; clearInterval(timer); focusHeading();
  }
}
function start() {
  cancelIntro(); clearInterval(timer); recorded = false;
  sessionId = crypto.randomUUID(); started = new Date().toLocaleString();
  engine.start(); sync(); view.value = 'practice';
  timer = setInterval(() => { engine.tick(); sync(); }, 50); focusHeading();
}
function pause() { engine.pause(); sync(); }
function resume() { if (!support.value) { engine.resume(); sync(); } }
function stop() { engine.stop(); sync(); }
async function openSupport(event) {
  supportTrigger = event.currentTarget;
  if (active.value) pause();
  support.value = true; await nextTick(); supportHeading.value?.focus();
}
async function closeSupport() { support.value = false; await nextTick(); supportTrigger?.focus(); }
function navigate(destination) { view.value = destination; focusHeading(); }
const mode = ref('success'), introState = ref('idle'), intro = ref('');
const requests = new LatestRequest(); let introTimer, settleIntro;
function cancelIntro() { requests.cancel(); clearTimeout(introTimer); settleIntro?.(''); settleIntro = null; introState.value = 'idle'; intro.value = ''; }
function requestIntro() {
  if (introState.value === 'loading') return;
  const selectedMode = mode.value; introState.value = 'loading'; intro.value = '';
  requests.run(() => new Promise((resolve, reject) => {
    settleIntro = resolve;
    introTimer = setTimeout(() => selectedMode === 'failed' ? reject(new Error('Simulated connection failure.')) : resolve('This practice has six cycles: breathe in for four seconds, then out for six. You can pause or stop at any time. The circle is optional.'), selectedMode === 'delayed' ? 8000 : 500);
  }), ({ value, error }) => { introState.value = error ? 'failed' : 'success'; intro.value = error ? error.message : value; });
}
onUnmounted(() => { clearInterval(timer); cancelIntro(); });
</script>

<template>
  <div class="shell">
    <header class="topbar">
      <a class="brand" href="#main" aria-label="A little space, skip to main content"><span class="brand-mark" aria-hidden="true">◒</span> a little space<span class="brand-dot">.</span></a>
      <span class="demo-tag">COURSEWORK DEMO</span>
    </header>
    <div class="workspace">
      <aside class="sidebar" aria-label="Prototype navigation">
        <p class="eyebrow">YOUR SPACE</p>
        <nav aria-label="Main navigation">
          <button :class="{ selected: view === 'practice' }" @click="navigate('practice')" :aria-current="view === 'practice' ? 'page' : undefined"><span aria-hidden="true">◉</span> Practice</button>
          <button :disabled="active" :class="{ selected: view === 'history' }" @click="navigate('history')" :aria-current="view === 'history' ? 'page' : undefined"><span aria-hidden="true">≡</span> Session history</button>
        </nav>
        <p v-if="active" class="small muted">History is available after stopping or completing.</p>
        <div class="sidebar-note"><span class="tiny-line"></span><p>A moment of practice.<br>At your own pace.</p><p class="small muted">A fictional coursework experience, not therapy or a monitored service.</p></div>
      </aside>
      <main id="main" tabindex="-1">
        <div class="page-top"><span class="eyebrow">{{ view === 'history' ? 'YOUR RECORDS' : 'A MOMENT TO PRACTICE' }}</span><button class="support-link" @click="openSupport">Crisis support <span aria-hidden="true">↗</span></button></div>
        <section v-if="support" class="support-panel" aria-labelledby="support-title" @keydown.esc="closeSupport">
          <div class="panel-heading"><h2 id="support-title" ref="supportHeading" tabindex="-1">Crisis support</h2><button class="secondary" @click="closeSupport">Close support</button></div>
          <p v-if="active">Practice is paused. Closing this panel will not resume it. Use Resume when you choose.</p>
          <p>This demo is not monitored. The following resource serves the United States and its territories.</p>
          <p><strong>988 Suicide &amp; Crisis Lifeline</strong></p>
          <div class="support-actions"><a href="tel:988?oai_link_source=model_response_hotline">Call 988</a><a href="sms:988?oai_link_source=model_response_hotline">Text 988</a><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">Online chat ↗</a></div>
          <p class="small">Resource checked through the helpline lookup on October 15, 2026. Availability was not tested by contacting the service.</p>
          <button v-if="active" class="stop" @click="stop">Stop practice</button>
        </section>
        <template v-if="view === 'practice'">
          <div class="title-block"><h1 ref="heading" tabindex="-1">{{ active ? 'One breath at a time.' : finished ? (exercise.state === 'completed' ? 'Practice completed.' : 'Practice stopped.') : 'Make a little space.' }}</h1><p>{{ active ? 'Follow the cue. Pause or stop whenever you choose.' : finished ? 'You choose what comes next.' : 'A short breathing practice, with room to go at your own pace.' }}</p></div>
          <section class="practice-card" aria-label="Breathing practice">
            <div class="card-meta"><span class="pill">{{ active ? 'IN PRACTICE' : finished ? 'SESSION RESULT' : 'PACED BREATHING' }}</span><span class="small muted">{{ active ? `Cycle ${exercise.cycle} of 6` : '60 seconds · 6 cycles' }}</span></div>
            <div class="practice-body">
              <div class="orb-wrap" aria-hidden="true"><div class="orb" :style="{ transform: `scale(${cueScale})` }" :class="{ moving: active && !reduceMotion, paused: exercise.state === 'paused', inhale: exercise.phase === 'Breathe in' }"><div class="orb-inner"><span>{{ active ? (exercise.state === 'paused' ? 'Ⅱ' : exercise.count) : finished ? '✓' : '4 / 6' }}</span><small>{{ active ? (exercise.state === 'paused' ? 'paused' : 'seconds') : finished ? exercise.state : 'in · out' }}</small></div></div></div>
              <div class="practice-copy">
                <template v-if="!active && !finished"><h2>60-second breathing practice</h2><p>Breathe in for four seconds.<br>Breathe out for six.<br>We’ll guide you through six cycles.</p><button class="primary" :disabled="support" @click="start">Start practice <span aria-hidden="true">→</span></button><p class="small muted">No check-in or typing needed.</p></template>
                <template v-else-if="active"><p class="eyebrow">{{ exercise.state === 'paused' ? 'TAKE YOUR TIME' : 'CURRENT STEP' }}</p><h2 role="status">{{ exercise.state === 'paused' ? 'Paused' : exercise.phase }}</h2><p class="counter-text">{{ exercise.state === 'paused' ? 'Resume only when you choose.' : `${exercise.count} seconds · ${exercise.remaining} seconds remaining` }}</p><div class="exercise-actions"><button v-if="exercise.state === 'running'" class="primary" @click="pause">Pause</button><button v-else class="primary" :disabled="support" @click="resume">Resume</button><button class="stop" @click="stop">Stop practice</button></div><p v-if="support" class="small">Close support to enable Resume.</p></template>
                <template v-else><h2>{{ exercise.state === 'completed' ? 'Six cycles completed.' : 'Stopped, on your terms.' }}</h2><p>{{ Math.floor(exercise.elapsed / 1000) }} seconds of active practice.<br>Added to this tab’s temporary history.</p><div class="exercise-actions"><button class="primary" :disabled="support" @click="start">Practice again</button><button class="secondary" @click="navigate('history')">View history</button></div></template>
              </div>
            </div>
            <div v-if="active" class="progress-track" role="progressbar" aria-label="Practice progress" :aria-valuenow="Math.floor(exercise.elapsed / 1000)" :aria-valuemax="60" aria-valuemin="0"><div :style="{ width: `${exercise.elapsed / 600}%` }"></div></div>
            <div class="card-bottom"><label class="motion-control"><input type="checkbox" v-model="reduceMotion"> Use a still cue</label><span class="small muted">{{ reduceMotion ? 'Text + countdown. No animation.' : 'Gentle motion + countdown' }}</span></div>
          </section>
          <section v-if="!active" class="intro-card" aria-labelledby="intro-heading"><div><span class="eyebrow">OPTIONAL INTRODUCTION</span><h2 id="intro-heading">A little guidance before you begin</h2><p class="small muted">Scripted demo only. No AI provider or saved conversation.</p></div><div class="mock-controls"><label for="mock-mode">Demo response</label><select id="mock-mode" v-model="mode" @change="cancelIntro"><option value="success">Success</option><option value="failed">Failed</option><option value="delayed">Delayed (8 seconds)</option></select><button class="secondary" @click="requestIntro" :disabled="introState === 'loading'">{{ introState === 'loading' ? 'Waiting…' : introState === 'idle' ? 'Show introduction' : 'Retry introduction' }}</button></div><div role="status" class="intro-response" v-if="introState !== 'idle'"><template v-if="introState === 'loading'">Waiting for a mock response. You can start practice now.</template><template v-else-if="introState === 'failed'">{{ intro }} Change the mode to Success and retry, or start practice.</template><template v-else>{{ intro }}</template></div></section>
        </template>
        <template v-else><div class="title-block"><h1 ref="heading" tabindex="-1">Your practice, recorded.</h1><p>Duration and status only. These records don’t measure wellbeing.</p></div><section class="history-card"><div class="panel-heading"><h2>Session history</h2><span class="pill">TEMPORARY DEMO</span></div><div class="table-scroll"><table><caption class="small muted">Fictional example + sessions from this tab. All reset on refresh.</caption><thead><tr><th scope="col">Session</th><th scope="col">Duration</th><th scope="col">Status</th></tr></thead><tbody><tr v-for="row in history" :key="row.id"><td>{{ row.started }}<small>{{ row.fixture ? 'Fictional fixture' : 'This tab · not saved to a database' }}</small><code>{{ row.id }}</code></td><td>{{ row.duration }}s</td><td><span class="status-chip">{{ row.status }}</span></td></tr></tbody></table></div><button class="secondary" @click="navigate('practice')">Back to practice</button></section></template>
        <footer><span class="footer-dot" aria-hidden="true"></span><p><strong>Prototype, not a support service.</strong> History, preferences, and mock responses reset on refresh. No backend, database, or live AI is connected.</p></footer>
      </main>
    </div>
  </div>
</template>
