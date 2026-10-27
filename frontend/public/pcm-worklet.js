// Audio remains in memory; main thread controls collection and turn boundaries.
class PCM extends AudioWorkletProcessor {
  process(inputs) {
    const channel=inputs[0]?.[0];
    if(channel) this.port.postMessage(channel.slice());
    return true;
  }
}
registerProcessor('pcm-capture',PCM);
