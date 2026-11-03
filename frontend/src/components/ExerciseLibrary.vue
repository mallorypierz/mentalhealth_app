<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue';
import { decide, ACTIVITIES } from '../recommendation.js';
import { api } from '../api.js';
import { getAccess } from '../identityAccess.js';
import { EXERCISES } from '../exercises.js';
const emit = defineEmits(['practice']);
const guest = getAccess()?.mode !== 'profile';
const saved = ref(null), remember = ref(false), pending = ref(null), busy = ref(false), notice = ref(''), recent = ref([]), historyError = ref(false);
let alive = true, loadVersion = 0;
onUnmounted(() => { alive = false; });
async function loadPreferences() {
  const version = ++loadVersion;
  try { const value = await api('/preferences'); if (alive && version === loadVersion) { saved.value = value; notice.value = ''; } }
  catch { if (alive && version === loadVersion) notice.value = 'Saved preferences could not load. Your current answers still work.'; }
}
onMounted(async () => {
  loadPreferences();
  try { const value = await api('/sessions?limit=5'); if (alive) recent.value = value.sessions; }
  catch { if (alive) historyError.value = true; }
});
function useSaved() {
  if (!saved.value?.answers) return;
  activity.value = saved.value.answers.activity; breath.value = saved.value.answers.breath;
  quiz.value = true; result.value = false; step.value = 0; focusQuestion();
}
async function persist(forget = false, retry = false) {
  if (guest || busy.value || !saved.value) return;
  if (!retry) pending.value = { operation_id: crypto.randomUUID(), expected_revision: saved.value.revision, answers: forget ? null : { activity: activity.value, breath: breath.value } };
  ++loadVersion; busy.value = true;
  try {
    const value = await api('/preferences', 'PUT', pending.value);
    if (!alive) return;
    saved.value = value; pending.value = null; remember.value = false;
    notice.value = value.answers ? 'Preferences saved.' : 'Remembered preferences forgotten. Current answers remain only for this visit.';
  } catch (error) {
    if (alive) notice.value = 'Preference change not confirmed. Retry the same change, or reload saved preferences. Current answers still work.';
  } finally { if (alive) busy.value = false; }
}

const step = ref(0), questionHeading = ref(null);
async function focusQuestion() { await nextTick(); questionHeading.value?.focus(); }
function moveStep(value) { step.value = value; focusQuestion(); }
function showResult() { result.value = true; focusQuestion(); }
const quiz = ref(false), result = ref(false), activity = ref(''), breath = ref('');
const decision = computed(() => decide(activity.value, breath.value));
const suggestion = computed(() => decision.value.exercise);
function retake() { activity.value = ''; breath.value = ''; result.value = false; quiz.value = true; step.value = 0; focusQuestion(); }
</script>

<template>
  <section class="history-card" aria-labelledby="library-heading">
    <h1 id="library-heading">Exercise library</h1>
    <template v-if="!quiz">
      <p>Choose an exercise, or find a suggestion.</p>
      <button class="primary" @click="retake">Help me choose</button>
    </template>
    <form v-if="quiz" class="quiz" @submit.prevent="step === 0 ? moveStep(1) : showResult()">
      <template v-if="!result">
        <p class="step-count">{{ step + 1 }} of 2 · Optional</p>
        <h2 ref="questionHeading" tabindex="-1">{{ step === 0 ? 'What would you like to try?' : 'Is focusing on breathing comfortable today?' }}</h2>
        <fieldset v-if="step === 0">
          <legend class="sr-only">Preferred activity</legend>
          <label v-for="item in ACTIVITIES" :key="item[0]" class="quiz-option"><input type="radio" v-model="activity" :value="item[0]"> {{ item[1] }}</label>
          <label class="quiz-option"><input type="radio" v-model="activity" value="none"> No preference</label>
        </fieldset>
        <fieldset v-else>
          <legend class="sr-only">Comfort with breathing</legend>
          <label v-for="item in [['yes','Yes'],['avoid','I’d rather avoid it'],['unsure','Not sure'],['none','No preference']]" :key="item[0]" class="quiz-option"><input type="radio" v-model="breath" :value="item[0]"> {{ item[1] }}</label>
        </fieldset>
        <div class="quiz-actions">
          <button v-if="step" class="secondary" type="button" @click="moveStep(0)">Back</button>
          <button class="primary" type="submit">{{ step === 0 ? 'Next' : 'See suggestion' }}</button>
          <button class="secondary" type="button" @click="step === 0 ? (activity = '', moveStep(1)) : (breath = '', showResult())">Skip question</button>
        </div>
        <button class="text-button" type="button" @click="quiz = false; result = false">Skip quiz</button>
      </template>
      <div v-else>
        <p class="step-count">Your suggestion</p>
        <h2 ref="questionHeading" tabindex="-1">{{ suggestion ? suggestion.name : 'Choose what suits you' }}</h2>
        <p>{{ decision.reason }}</p>
        <div class="quiz-actions">
          <button v-if="suggestion" type="button" class="primary" @click="emit('practice', suggestion.key)">Preview exercise</button>
          <button type="button" class="secondary" @click="quiz = false; result = false">Choose another</button>
        </div>
        <button type="button" class="text-button" @click="result = false; moveStep(0)">Change answers</button>
        <button type="button" class="text-button" @click="retake">Start quiz over</button>
      </div>
    </form>
    <details v-if="!quiz || result" class="library-details">
      <summary>Saved preferences</summary>
    <section aria-label="Remembered preferences" :data-preference-id="saved?.id">

      <p v-if="guest">Guest answers aren’t saved. Use a profile to remember them.</p>
      <template v-else>
        <p>Saved answers are used only when you choose.</p>
        <button v-if="saved?.answers" class="secondary" @click="useSaved">Use saved answers</button>
        <button v-if="saved?.answers" class="secondary" :disabled="busy || !!pending" @click="persist(true)">Forget saved answers</button>
        <label><input type="checkbox" v-model="remember"> Remember these answers</label>
        <button class="primary" :disabled="!remember || !saved || busy || !!pending" @click="persist()">Save preferences</button>
      </template>
      <p role="status">{{ busy ? 'Saving preferences…' : notice }}</p>
      <button v-if="pending" class="secondary" :disabled="busy" @click="persist(false, true)">Retry same preference change</button>
      <button v-if="!guest && notice" class="secondary" :disabled="busy" @click="pending = null; loadPreferences()">Reload saved preferences</button>
    </section>
    </details>
    <details v-if="!quiz" class="library-details"><summary>Previous exercises</summary><section aria-label="Previous exercise choices"><p>History doesn’t affect suggestions or measure wellbeing.</p><p v-if="historyError" role="status">History could not load.</p><p v-else-if="!recent.length">No previous choices loaded.</p><ul><li v-for="row in recent" :key="row.id" :data-session-id="row.id">{{ EXERCISES.find(x => x.key === row.skill_key)?.name || row.skill_key }} · {{ row.status }} · {{ row.active_duration_ms / 1000 }} seconds <time :datetime="row.started_at">{{ new Date(row.started_at).toLocaleString() }}</time><small>Record {{ row.id }}</small></li></ul></section></details>
    <ul v-if="!quiz" class="exercise-library">
      <li v-for="exercise in EXERCISES" :key="exercise.key">
        <h2>{{ exercise.name }}</h2>
        <p>{{ exercise.duration / 1000 }} seconds · {{ exercise.summary }}</p>
        <button class="primary" @click="emit('practice', exercise.key)">Open {{ exercise.name }}</button>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.quiz { max-width: 36rem; margin: 1.5rem 0; }
.quiz h2 { font-size: 1.5rem; line-height: 1.3; }
.step-count { font-size: .9rem; }
.quiz fieldset { border: 0; padding: 0; margin: 1rem 0; }
.quiz-option { display: flex; align-items: center; gap: .65rem; padding: .85rem; margin: .5rem 0; border: 1px solid #78846f; border-radius: .65rem; cursor: pointer; }
.quiz-option:has(input:checked) { background: #e7eddf; border-color: #405138; }
.quiz-option:focus-within { outline: 2px solid #405138; outline-offset: 2px; }
.quiz-actions { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1rem 0; }
.text-button { background: transparent; border: 0; text-decoration: underline; padding: .75rem; color: inherit; cursor: pointer; }
.library-details { margin: 1.25rem 0; }
.library-details summary { cursor: pointer; padding: .5rem 0; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); }
.exercise-library { list-style: none; padding: 0; margin: 0; }
.exercise-library > li { padding: 1.25rem 0; border-top: 1px solid #dce3d6; }
.exercise-library h2 { font-size: 1.3rem; overflow-wrap: anywhere; }
.exercise-library button { max-width: 100%; white-space: normal; }
</style>
