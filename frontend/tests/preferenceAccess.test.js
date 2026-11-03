import test from 'node:test';
import assert from 'node:assert/strict';
import { api } from '../src/api.js';
import { setAccess } from '../src/identityAccess.js';
test('late preference response is rejected after identity changes', async()=>{
 globalThis.sessionStorage={setItem(){}};
 setAccess({access_token:'fictional-a',context_version:1});
 let resolve;
 globalThis.fetch=()=>new Promise(r=>{resolve=r;});
 const request=api('/preferences');
 setAccess({access_token:'fictional-b',context_version:2});
 resolve({ok:true,json:async()=>({answers:{activity:'stop',breath:'yes'}})});
 await assert.rejects(request,/Profile changed/);
});
