// Reviewed November 2, 2026. See docs/design-pipeline.md for sources/approval.
// These are guided sequences, not evidence that an activity helped or was done.
export const EXERCISES = Object.freeze([
  { key: 'paced_breathing_4_6', name: 'Paced breathing (4–6)', duration: 60000, breathFocused: true,
    summary: 'A breathing rhythm with six cycles and an optional moving cue.', steps: [] },
  { key: 'sensory_grounding_5_4_3_2_1', name: '5-4-3-2-1 sensory grounding', duration: 75000, breathFocused: false,
    summary: 'Five prompts about your surroundings. Nothing to fetch or consume.', steps: [
      { title: '5 things you can see', text: 'Notice five things you can see around you.', duration: 15000 },
      { title: '4 things you can feel', text: 'Notice four things you can feel, such as contact with your chair or clothing.', duration: 15000 },
      { title: '3 things you can hear', text: 'Notice three sounds around you.', duration: 15000 },
      { title: '2 things you can smell', text: 'Notice two smells where you are. There is no need to find or fetch anything.', duration: 15000 },
      { title: '1 thing you can taste', text: 'Notice one taste already present. There is no need to eat or drink anything.', duration: 15000 },
    ] },
  { key: 'stop', name: 'STOP', duration: 60000, breathFocused: true,
    summary: 'Four prompts for pausing before an action. Includes a breath-focused step.', steps: [
      { title: 'S · Stop', text: 'Pause before reacting. Give yourself a moment before taking action.', duration: 15000 },
      { title: 'T · Take a step back', text: 'Take a step back from the situation and take a breath.', duration: 15000 },
      { title: 'O · Observe', text: 'Notice your thoughts, feelings, and what is happening around you.', duration: 15000 },
      { title: 'P · Proceed mindfully', text: 'Consider your goal and choose your next action deliberately.', duration: 15000 },
    ] },
  { key: 'cognitive_reframe', name: 'One-minute cognitive reframe', duration: 60000, breathFocused: false,
    summary: 'Three prompts for looking at a thought from another angle. No typing required.', steps: [
      { title: 'Notice a thought', text: 'Bring one thought to mind. You do not need to write it down or share it.', duration: 20000 },
      { title: 'Check the evidence', text: 'What makes this thought seem true? Could there be another way to explain what happened?', duration: 20000 },
      { title: 'Try another perspective', text: 'Try a balanced alternative. You do not have to change the thought.', duration: 20000 },
    ] },
]);
export const exerciseByKey = key => EXERCISES.find(exercise => exercise.key === key);
