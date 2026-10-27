import test from 'node:test';
import assert from 'node:assert/strict';
import {Segmenter,wavBytes,Microphone,acceptsMicrophoneInput} from '../src/microphone.js';

test('PCM WAV is mono 16kHz 16-bit with bounded sample values',()=>{
 const bytes=wavBytes([0,2,-2]), v=new DataView(bytes.buffer);
 assert.equal(v.getUint32(24,true),16000); assert.equal(v.getUint16(22,true),1);
 assert.equal(v.getUint32(40,true),6); assert.equal(v.getInt16(46,true),32767);
});
test('silence does not submit and a short silence ends one voiced utterance',()=>{
 let turns=[],onsets=0; const s=new Segmenter(v=>turns.push(v),()=>onsets++);
 for(let i=0;i<30;i++) s.push(Array(1600).fill(0));
 assert.equal(turns.length,0);
 for(let i=0;i<4;i++) s.push(Array(1600).fill(.1));
 for(let i=0;i<9;i++) s.push(Array(1600).fill(0));
 assert.equal(turns.length,1); assert.equal(onsets,1);
 for(let i=0;i<20;i++) s.push(Array(1600).fill(0));
 assert.equal(turns.length,1);
});
test('turn duration is bounded and reset discards unsubmitted audio',()=>{
 const turns=[]; const s=new Segmenter(v=>turns.push(v),()=>{});
 for(let i=0;i<300;i++) s.push(Array(1600).fill(.1));
 assert.equal(turns[0].length,960044);
 s.push(Array(1600).fill(.1)); s.reset();
 for(let i=0;i<10;i++) s.push(Array(1600).fill(0));
 assert.equal(turns.length,1);
});
test('stop during permission prompt closes a late microphone without starting capture',async()=>{
 let resolve,stopped=0;
 Object.defineProperty(globalThis,'navigator',{configurable:true,value:{mediaDevices:{getUserMedia:()=>new Promise(r=>resolve=r)}}});
 const mic=new Microphone({send(){},onset(){},failed(){}});
 const start=mic.start(); await mic.stop();
 resolve({getTracks:()=>[{stop(){stopped++;}}]});
 assert.equal(await start,false); assert.equal(stopped,1);
});

test('reply loading/playback blocks capture; finish or manual stop resumes only an active visible session',()=>{
 const state={live:true,phase:'ready',playback:'playing',suspended:false,hidden:false};
 for(const playback of ['loading','playing']) assert.equal(acceptsMicrophoneInput({...state,playback}),false);
 for(const playback of ['finished','stopped','failed']) {
  assert.equal(acceptsMicrophoneInput({...state,playback}),true);
  assert.equal(acceptsMicrophoneInput({...state,playback,hidden:true}),false);
  assert.equal(acceptsMicrophoneInput({...state,playback,suspended:true}),false);
  for(const phase of ['stopped','failed','processing','held']) assert.equal(acceptsMicrophoneInput({...state,playback,phase}),false);
 }
});
