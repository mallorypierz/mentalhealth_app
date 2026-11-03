import test from 'node:test';
import assert from 'node:assert/strict';
import { Exercise } from '../src/exercise.js';
import { EXERCISES } from '../src/exercises.js';
import { recommend } from '../src/recommendation.js';
test('all reviewed steps appear in order and each sequence completes at its duration',()=>{
 for(const skill of EXERCISES.slice(1)) {
 let t=0; const e=new Exercise(()=>t,skill.key);e.start();
 for(let i=0;i<skill.steps.length;i++){assert.equal(e.tick().stepIndex,i);t+=skill.steps[i].duration;}
 assert.equal(e.tick().state,'completed');assert.equal(e.elapsed,skill.duration);
 e.start();t+=1000;e.pause();t+=90000;assert.equal(e.tick().elapsed,1000);e.stop();assert.equal(e.state,'stopped');
 }
});
test('preferences never automatically recommend breath focus when avoided or uncertain',()=>{
 for(const activity of ['',...EXERCISES.map(x=>x.key)]) for(const breath of ['avoid','unsure']) assert.ok(!recommend(activity,breath)?.breathFocused);
 assert.equal(recommend('cognitive_reframe','yes').key,'cognitive_reframe');
 assert.equal(recommend('','yes').key,'paced_breathing_4_6');assert.equal(recommend('',''),null);
});

test('grounding next steps preserve actual time, pause, restart and timer boundary',()=>{
 let t=0; const e=new Exercise(()=>t,'sensory_grounding_5_4_3_2_1');e.start();
 t=2000;e.nextStep();assert.equal(e.snapshot().stepIndex,1);assert.equal(e.elapsed,2000);
 e.pause();t=9000;e.nextStep();assert.equal(e.snapshot().stepIndex,1);e.resume();
 for(let i=1;i<5;i++){t+=1000;e.nextStep();}
 assert.equal(e.state,'completed');assert.equal(e.elapsed,6000);
 e.start();assert.equal(e.snapshot().stepIndex,0);assert.equal(e.offset,0);
 t+=15000;e.nextStep();assert.equal(e.snapshot().stepIndex,1);
 t+=60000;assert.equal(e.tick().state,'completed');assert.equal(e.elapsed,75000);
 const breathing=new Exercise(()=>t);breathing.start();breathing.nextStep();assert.equal(breathing.state,'running');assert.equal(breathing.offset,0);
});
