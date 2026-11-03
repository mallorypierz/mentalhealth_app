import test from 'node:test';
import assert from 'node:assert/strict';
import { restoreIdentity } from '../src/identityRecovery.js';
test('revoked browser access is cleared once and returns a fresh chooser without replaying writes', async () => {
 let access = {access_token:'fictional-stale'}; const calls=[];
 const result=await restoreIdentity(async(path,method,body)=>{
  calls.push([path,method]);
  if(path==='/identity') throw Object.assign(new Error('revoked'),{status:401});
  assert.equal(access,null); assert.ok(body.bootstrap_id); return {mode:'chooser'};
 },()=>access,()=>{access=null;});
 assert.equal(result.mode,'chooser');
 assert.deepEqual(calls,[['/identity',undefined],['/identity/bootstrap','POST']]);
});
test('network and server failures preserve credentials and do not bootstrap',async()=>{
 for(const status of [undefined,403,500]) {
  let cleared=false,calls=0;
  await assert.rejects(restoreIdentity(async()=>{calls++;throw Object.assign(new Error('failed'),{status});},()=>({access_token:'fictional'}),()=>{cleared=true;}));
  assert.equal(cleared,false);assert.equal(calls,1);
 }
});
test('valid identity is retained; failed bootstrap is not retried in a loop',async()=>{
 const identity={mode:'profile'};
 assert.equal(await restoreIdentity(async()=>identity,()=>({access_token:'fictional'}),()=>assert.fail()),identity);
 let calls=0;
 await assert.rejects(restoreIdentity(async()=>{calls++;throw Object.assign(new Error('revoked'),{status:401});},()=>({access_token:'fictional'}),()=>{}));
 assert.equal(calls,2);
});
