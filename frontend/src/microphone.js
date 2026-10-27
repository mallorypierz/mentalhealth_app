// Reply audio must never become a new microphone turn.
export function acceptsMicrophoneInput({live, phase, playback, suspended, hidden}) {
  return live && ['ready','listening'].includes(phase) &&
    !['loading','playing'].includes(playback) && !suspended && !hidden;
}
// One explicitly started microphone session. No provider calls in this module.
export function wavBytes(samples) {
  const buffer=new ArrayBuffer(44+samples.length*2), view=new DataView(buffer);
  const text=(offset,value)=>[...value].forEach((c,i)=>view.setUint8(offset+i,c.charCodeAt(0)));
  text(0,'RIFF'); view.setUint32(4,36+samples.length*2,true); text(8,'WAVE'); text(12,'fmt ');
  view.setUint32(16,16,true); view.setUint16(20,1,true); view.setUint16(22,1,true);
  view.setUint32(24,16000,true); view.setUint32(28,32000,true); view.setUint16(32,2,true); view.setUint16(34,16,true);
  text(36,'data'); view.setUint32(40,samples.length*2,true);
  samples.forEach((n,i)=>view.setInt16(44+i*2,Math.max(-1,Math.min(1,n))*32767,true));
  return new Uint8Array(buffer);
}
export class Segmenter {
  constructor(send, onset) { this.send=send; this.onset=onset; this.reset(); }
  reset() { this.samples=[]; this.silent=0; this.started=false; this.voiced=0; }
  push(samples) {
    const rms=Math.sqrt(samples.reduce((n,x)=>n+x*x,0)/samples.length);
    const talking=rms>0.018;
    if(talking && !this.started) { this.started=true; this.onset(); }
    if(!this.started) return;
    this.samples.push(...samples);
    if(talking) { this.silent=0; this.voiced+=samples.length; } else this.silent+=samples.length;
    if(this.silent>=14400 || this.samples.length>=480000) {
      const value=this.samples.slice(0,480000), valid=this.voiced>=3200;
      this.reset(); if(valid) this.send(wavBytes(value));
    }
  }
}
export class Microphone {
  constructor({send,onset,failed,accepting=()=>true}) {
    Object.assign(this,{send,onset,failed,accepting}); this.generation=0;
  }
  async start() {
    const generation=++this.generation;
    if(!navigator.mediaDevices?.getUserMedia) throw new Error('Microphone access is unavailable in this browser. Type instead.');
    const stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,channelCount:1}});
    if(generation!==this.generation) { stream.getTracks().forEach(t=>t.stop()); return false; }
    this.stream=stream;
    try {
      const context=new AudioContext(); this.context=context;
      await context.audioWorklet.addModule('/pcm-worklet.js');
      if(generation!==this.generation) { await this.stop(); return false; }
      this.segmenter=new Segmenter(this.send,this.onset);
      let input=[],position=0;
      const ratio=context.sampleRate/16000;
      this.node=new AudioWorkletNode(context,'pcm-capture');
      this.node.port.onmessage=event=>{
        if(generation!==this.generation) return;
        if(!this.accepting()) { this.segmenter.reset(); input=[]; position=0; return; }
        input.push(...event.data); const out=[];
        while(position+1<input.length) {
          const i=Math.floor(position), f=position-i;
          out.push(input[i]*(1-f)+input[i+1]*f); position+=ratio;
        }
        const consumed=Math.floor(position); input=input.slice(consumed); position-=consumed;
        if(out.length) this.segmenter.push(out);
      };
      this.source=context.createMediaStreamSource(stream); this.source.connect(this.node);
      // A silent destination keeps processing active without monitoring microphone audio.
      this.gain=context.createGain(); this.gain.gain.value=0; this.node.connect(this.gain); this.gain.connect(context.destination);
      stream.getTracks().forEach(track=>{ track.onended=()=>{ if(generation===this.generation) { this.stop(); this.failed('Microphone disconnected. Start again explicitly or type instead.'); } }; });
      await context.resume();
      if(generation!==this.generation) return false;
      return true;
    } catch(error) { await this.stop(); throw error; }
  }
  async stop() {
    ++this.generation; this.segmenter?.reset();
    this.stream?.getTracks().forEach(t=>t.stop()); this.stream=null;
    this.node?.disconnect(); this.source?.disconnect(); this.gain?.disconnect();
    if(this.context && this.context.state!=='closed') await this.context.close();
    this.context=null;
  }
}
