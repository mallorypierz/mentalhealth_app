// A limited wording rule, not assessment or reliable crisis detection.
export const CRISIS_PHRASES = ['kill myself', 'end my life', 'hurt myself', 'suicide', 'suicidal'];
export function matchesCrisisPhrase(text) {
  const normalized = text.toLowerCase().replace(/\s+/g, ' ').trim();
  return CRISIS_PHRASES.some(phrase => normalized.includes(phrase));
}
export const CRISIS_NOTICE = 'This message was not sent to AI or saved. You can open Crisis support for human-support options.';
