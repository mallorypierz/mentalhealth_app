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

test('approved indirect wording and apostrophe variants match; misrecognition is not assumed safe', () => {
  for (const text of ["I don't want to be alive", 'I don’t want to be alive', 'I do not want to be alive', 'I might do something to myself']) {
    assert.equal(matchesCrisisPhrase(text), true);
  }
  assert.equal(matchesCrisisPhrase('Fictional: I might do something to my shelf'), false);
  assert.equal(matchesCrisisPhrase('Fictional: I wish I could disappear'), false);
  assert.equal(matchesCrisisPhrase('Quote: “I don’t want to be alive.”'), true);
  assert.equal(matchesCrisisPhrase('I am not going to hurt myself.'), true);
});
