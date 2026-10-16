import test from 'node:test';
import assert from 'node:assert/strict';
import { Exercise, LatestRequest } from '../src/exercise.js';
test('six 4/6 cycles complete at exactly 60 seconds', () => {
 let time=0; const e=new Exercise(()=>time); e.start();
 for(let cycle=0;cycle<6;cycle++) {
  time=cycle*10000; assert.equal(e.tick().phase,'Breathe in'); assert.equal(e.tick().cycle,cycle+1);
  time+=3999; assert.equal(e.tick().phase,'Breathe in');
  time+=1; assert.equal(e.tick().phase,'Breathe out'); assert.equal(e.tick().count,6);
  time=cycle*10000+9999; assert.equal(e.tick().state,'running');
 }
 time=60000; assert.equal(e.tick().state,'completed'); assert.equal(e.elapsed,60000);
});
test('pause excludes elapsed time, stop is final, restart resets time',()=>{
 let time=0; const e=new Exercise(()=>time);e.start();time=4500;e.pause();time=200000;e.tick();assert.equal(e.elapsed,4500);e.resume();time+=500;e.stop();assert.equal(e.elapsed,5000);assert.equal(e.state,'stopped');time+=80000;e.tick();assert.equal(e.elapsed,5000);e.start();assert.equal(e.elapsed,0);
});
test('late responses cannot update state after cancellation or replacement', async()=>{
 const r=new LatestRequest();let resolve;const applied=[];
 const first=r.run(()=>new Promise(res=>resolve=res),x=>applied.push(x));r.cancel();resolve('old');await first;assert.deepEqual(applied,[]);
 let late;const next=r.run(()=>new Promise(res=>late=res),x=>applied.push(x));await r.run(async()=> 'current',x=>applied.push(x));late('stale');await next;assert.deepEqual(applied,[{value:'current'}]);
});
test('provider failure is reported without an invented response',async()=>{
 const r=new LatestRequest();let result;await r.run(async()=>{throw new Error('failed')},x=>result=x);assert.equal(result.error.message,'failed');assert.equal(result.value,undefined);
});
