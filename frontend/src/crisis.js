// A limited wording rule, not assessment or reliable crisis detection.
export const CRISIS_PHRASES = [
  'kill myself', 'end my life', 'hurt myself', 'suicide', 'suicidal',
  "i don't want to be alive", 'i do not want to be alive', 'i might do something to myself',
];
export function matchesCrisisPhrase(text) {
  const normalized = String(text).toLowerCase().replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
  return CRISIS_PHRASES.some(phrase => normalized.includes(phrase));
}
export const CRISIS_NOTICE = 'Some of these words may refer to immediate distress or self-harm. I may have misunderstood, especially if speech was transcribed incorrectly. This app cannot assess your safety or provide crisis care. You can open Crisis support for human-support options.';
export const DETECTION_LIMITS = 'Speech recognition and wording checks can make mistakes or miss distress. You can open Crisis support at any time, even when no notice appears.';
