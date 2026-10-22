import test from 'node:test';
import assert from 'node:assert/strict';
import { SessionPersistence } from '../src/sessionPersistence.js';

function setup() {
  const entries = {};
  globalThis.localStorage = {
    setItem: (k, v) => { entries[k] = v; }, removeItem: k => { delete entries[k]; },
    getItem: k => entries[k] ?? null,
  };
  const records = new Map(), operations = new Map(), updates = [];
  let fail = false, loseResponse = false;
  globalThis.fetch = async (url, options) => {
    if (fail) throw new Error('offline');
    const body = options.body ? JSON.parse(options.body) : null;
    if (options.method === 'POST') {
      if (!records.has(body.session_id)) records.set(body.session_id, { id: body.session_id, status: 'in_progress', active_duration_ms: 0, paused_duration_ms: 0, revision: 1 });
      return { ok: true, json: async () => ({ session: records.get(body.session_id) }) };
    }
    const id = url.split('/').pop();
    if (options.method === 'PUT') {
      if (!operations.has(body.operation_id)) {
        const record = { ...records.get(id), ...body, revision: body.expected_revision + 1 };
        records.set(id, record); operations.set(body.operation_id, record);
      }
      if (loseResponse) { loseResponse = false; throw new Error('response lost after commit'); }
      return { ok: true, json: async () => ({ session: operations.get(body.operation_id) }) };
    }
    return { ok: true, json: async () => ({ session: records.get(id) }) };
  };
  return { service: new SessionPersistence(x => updates.push(x)), records, operations, updates,
    offline: value => { fail = value; }, loseNextResponse: () => { loseResponse = true; } };
}
const settle = () => new Promise(resolve => setTimeout(resolve, 5));

test('offline final outcome remains retryable and is saved once', async () => {
  const f = setup(); await f.service.begin('session-a', '2026-10-21T12:00:00Z'); await settle();
  f.offline(true); f.service.checkpoint('session-a', { state: 'stopped', elapsed: 12000, paused: 3000 }, '2026-10-21T12:00:15Z'); await settle();
  assert.equal(f.updates.at(-1).state, 'unknown');
  assert.equal(f.records.get('session-a').status, 'in_progress');
  f.offline(false); f.service.retry('session-a'); f.service.retry('session-a'); await settle();
  assert.equal(f.records.get('session-a').status, 'stopped'); assert.equal(f.operations.size, 1);
  assert.equal(f.updates.at(-1).state, 'saved');
});

test('lost commit response reuses exact operation instead of duplicating', async () => {
  const f = setup(); await f.service.begin('session-b', '2026-10-21T12:00:00Z'); await settle();
  f.loseNextResponse(); f.service.checkpoint('session-b', { state: 'completed', elapsed: 60000, paused: 0 }, '2026-10-21T12:01:00Z'); await settle();
  assert.equal(f.updates.at(-1).state, 'unknown');
  f.service.retry('session-b'); await settle();
  assert.equal(f.operations.size, 1); assert.equal(f.records.get('session-b').revision, 2);
  assert.equal(f.updates.at(-1).state, 'saved');
});

test('abandoned session uses only the database checkpoint and skips a live owner', async () => {
  const f = setup();
  const id = 'session-recovery';
  const key = 'coursework-session-outbox:' + id;
  f.records.set(id, {id, status:'in_progress', active_duration_ms:5000, paused_duration_ms:0, revision:2});
  const data = {create:{session_id:id, owner_token:'owner'}, saved:null,
    pending:{operation_id:'unsent-checkpoint', status:'in_progress', active_duration_ms:9000},
    desired:{status:'in_progress', active_duration_ms:10000}};
  localStorage.setItem(key, JSON.stringify(data));
  localStorage[key] = JSON.stringify(data);
  const previousNavigator = globalThis.navigator;
  Object.defineProperty(globalThis, 'navigator', {configurable:true, value:{locks:{request: async (key, options, fn) => fn(null)}}});
  await f.service.recover(); assert.equal(f.operations.size,0);
  navigator.locks.request = async (key, options, fn) => fn({name:key});
  await f.service.recover();
  assert.equal(f.records.get(id).status,'interrupted');
  assert.equal(f.records.get(id).active_duration_ms,5000);
  assert.equal(f.operations.size,1);
  Object.defineProperty(globalThis, 'navigator', {configurable:true, value:previousNavigator});
});
