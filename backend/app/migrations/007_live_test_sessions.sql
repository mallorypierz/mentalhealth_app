CREATE TABLE live_test_sessions (
 id TEXT PRIMARY KEY,
 label TEXT NOT NULL,
 call_limit INTEGER NOT NULL CHECK(call_limit BETWEEN 1 AND 50),
 budget_microdollars INTEGER NOT NULL CHECK(budget_microdollars BETWEEN 1 AND 2500000),
 state TEXT NOT NULL CHECK(state IN ('active','closed')),
 created_at TEXT NOT NULL
);
CREATE UNIQUE INDEX one_active_live_test_session ON live_test_sessions(state) WHERE state='active';
ALTER TABLE voice_provider_attempts ADD COLUMN test_session_id TEXT REFERENCES live_test_sessions(id);
CREATE INDEX attempts_by_test_session ON voice_provider_attempts(test_session_id);
