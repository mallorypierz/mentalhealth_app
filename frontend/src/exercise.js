import { exerciseByKey } from './exercises.js';
export const DURATION = 60000;
export class Exercise {
  constructor(now = () => performance.now(), skillKey = 'paced_breathing_4_6') { this.now = now; this.definition = exerciseByKey(skillKey); if (!this.definition) throw new Error('Unknown exercise'); this.offset = 0; this.state = 'ready'; this.elapsed = 0; this.anchor = 0; this.paused = 0; this.pauseAnchor = 0; }
  start() { this.offset = 0; this.elapsed = 0; this.paused = 0; this.anchor = this.now(); this.state = 'running'; }
  tick() {
    if (this.state === 'running') {
      const time = this.now(); this.elapsed = Math.min(this.definition.duration - this.offset, this.elapsed + time - this.anchor); this.anchor = time;
      if (this.elapsed + this.offset >= this.definition.duration) this.state = 'completed';
    }
    return this.snapshot();
  }
  nextStep() {
    if (this.definition.key !== 'sensory_grounding_5_4_3_2_1' || this.state !== 'running') return;
    const previous = this.snapshot().stepIndex;
    this.tick();
    // If the timer already advanced this step, do not skip another on a late click.
    if (this.state !== 'running' || this.snapshot().stepIndex !== previous) return;
    const boundary = this.definition.steps.slice(0, previous + 1).reduce((sum, step) => sum + step.duration, 0);
    this.offset = boundary - this.elapsed;
    if (previous === this.definition.steps.length - 1) this.state = 'completed';
  }
  pause() { this.tick(); if (this.state === 'running') { this.state = 'paused'; this.pauseAnchor = this.now(); } }
  resume() { if (this.state === 'paused') { this.paused += this.now() - this.pauseAnchor; this.anchor = this.now(); this.state = 'running'; } }
  stop() { if (this.state === 'paused') this.paused += this.now() - this.pauseAnchor; this.tick(); if (['running', 'paused'].includes(this.state)) this.state = 'stopped'; }
  snapshot() {
    const within = this.elapsed % 10000;
    const steps = this.definition.steps;
    let stepIndex = 0, stepStart = 0;
    while (stepIndex < steps.length - 1 && this.elapsed + this.offset >= stepStart + steps[stepIndex].duration) {
      stepStart += steps[stepIndex].duration; stepIndex++;
    }
    return { state: this.state, skillKey: this.definition.key, elapsed: this.elapsed, paused: this.paused + (this.state === 'paused' ? this.now() - this.pauseAnchor : 0), cycle: Math.min(6, Math.floor(this.elapsed / 10000) + 1), phase: within < 4000 ? 'Breathe in' : 'Breathe out', count: within < 4000 ? 4 - Math.floor(within / 1000) : 6 - Math.floor((within - 4000) / 1000), remaining: Math.ceil((this.definition.duration - this.elapsed - this.offset) / 1000), stepIndex, step: steps[stepIndex] || null };
  }
}
export class LatestRequest {
  version = 0;
  cancel() { this.version++; }
  async run(work, apply) {
    const version = ++this.version;
    try { const value = await work(); if (version === this.version) apply({ value }); }
    catch (error) { if (version === this.version) apply({ error }); }
  }
}
