import test from 'node:test';
import assert from 'node:assert/strict';
import { matchesCrisisPhrase } from '../src/crisis.js';

test('reviewed phrases match case and whitespace variants', () => {
  for (const text of ['Fictional: KILL MYSELF', 'end\nmy life', 'hurt myself', 'suicide', 'suicidal']) {
    assert.equal(matchesCrisisPhrase(text), true);
  }
});
test('rule limitations remain explicit: negation matches, indirect wording can miss', () => {
  assert.equal(matchesCrisisPhrase('Fictional quote: I am not suicidal.'), true);
  assert.equal(matchesCrisisPhrase('Fictional: I cannot go on.'), false);
  assert.equal(matchesCrisisPhrase('What happened in my last practice?'), false);
});
