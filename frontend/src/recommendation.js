import { EXERCISES } from './exercises.js';
export const ACTIVITIES = [
  ['paced_breathing_4_6', 'Follow a breathing rhythm'],
  ['sensory_grounding_5_4_3_2_1', 'Notice my surroundings'],
  ['stop', 'Pause before acting'],
  ['cognitive_reframe', 'Explore a different perspective'],
];
// Pure decision table: no network, storage, scoring, or generated instructions.
export function decide(activity = '', breath = '', available = EXERCISES) {
  const fallback = (status, reason) => ({ status, reason, exercise: null });
  if (!['', 'none', ...ACTIVITIES.map(x => x[0])].includes(activity) ||
      !['', 'none', 'yes', 'avoid', 'unsure'].includes(breath))
    return fallback('invalid', 'Please change your answers or choose an exercise.');
  const key = !activity || activity === 'none' ? (breath === 'yes' ? 'paced_breathing_4_6' : null) : activity;
  if (!key) return fallback('incomplete', ['avoid','unsure'].includes(breath)
    ? 'Grounding and reframing avoid breath focus. Choose either from the library.'
    : 'No clear match yet. Choose an exercise or change your answers.');
  const exercise = available.find(x => x.key === key);
  if (!exercise) return fallback('unavailable', 'That exercise is unavailable. Choose another from the library.');
  if (exercise.breathFocused && ['avoid', 'unsure'].includes(breath))
    return fallback('conflict', 'That activity includes breathing. Since you’d rather avoid it or aren’t sure, choose another or change your answers.');
  const chosen = ACTIVITIES.find(x => x[0] === activity);
  return { status: 'suggested', exercise, reason: chosen
    ? `You chose “${chosen[1]}”.${!exercise.breathFocused ? ' This activity does not focus on breathing.' : ''}`
    : 'You said yes to an exercise that focuses on breathing.' };
}
export const recommend = (activity, breath) => decide(activity, breath).exercise;
