import test from 'node:test';
import assert from 'node:assert/strict';
import { decide, ACTIVITIES } from '../src/recommendation.js';
import { EXERCISES } from '../src/exercises.js';
test('every activity/comfort combination obeys precedence and exclusions', () => {
 for (const [activity, label] of ACTIVITIES) for (const breath of ['', 'none', 'yes', 'avoid', 'unsure']) {
  const definition = EXERCISES.find(x=>x.key===activity);
  const result=decide(activity,breath);
  if (definition.breathFocused && ['avoid','unsure'].includes(breath)) {
   assert.equal(result.status,'conflict');assert.equal(result.exercise,null);
  } else {assert.equal(result.exercise.key,activity);assert.ok(result.reason.includes(label));}
 }
});
test('skips and neutral answers never fabricate an activity preference',()=>{
 for(const activity of ['', 'none']) for(const breath of ['', 'none','avoid','unsure']) assert.equal(decide(activity,breath).exercise,null);
 assert.equal(decide('','yes').exercise.key,'paced_breathing_4_6');
 assert.ok(decide('','yes').reason.includes('said yes'));
});
test('invalid and unavailable answers fail closed without arbitrary substitution',()=>{
 for(const args of [['invented','yes'],[null,'yes'],['stop','invented'],[{},'yes']]) assert.equal(decide(...args).status,'invalid');
 assert.equal(decide('stop','yes',EXERCISES.filter(x=>x.key!=='stop')).status,'unavailable');
 assert.equal(decide('','yes',[]).exercise,null);
});
test('changed answers produce a new decision without changing exercise instructions',()=>{
 const before=JSON.stringify(EXERCISES);
 assert.equal(decide('stop','yes').exercise.key,'stop');
 assert.equal(decide('stop','avoid').exercise,null);
 assert.equal(decide('cognitive_reframe','avoid').exercise.key,'cognitive_reframe');
 assert.equal(JSON.stringify(EXERCISES),before);
});
