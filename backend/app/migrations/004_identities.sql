-- Opt-in foundation only. Original owners remain legacy; no activity is reassigned.
ALTER TABLE demo_users ADD COLUMN kind TEXT NOT NULL DEFAULT 'legacy'
 CHECK(kind IN ('legacy', 'profile', 'guest'));
ALTER TABLE demo_users ADD COLUMN age INTEGER
 CHECK(age IS NULL OR (typeof(age) = 'integer' AND age BETWEEN 0 AND 120));
ALTER TABLE demo_users ADD COLUMN gender TEXT
 CHECK(gender IS NULL OR length(gender) BETWEEN 1 AND 60);
ALTER TABLE demo_users ADD COLUMN created_at TEXT;
ALTER TABLE demo_users ADD COLUMN updated_at TEXT;
ALTER TABLE demo_users ADD COLUMN revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1);

CREATE TABLE browser_sessions (
 id TEXT PRIMARY KEY,
 token_hash TEXT NOT NULL UNIQUE,
 active_owner_id TEXT REFERENCES demo_users(id),
 context_version INTEGER NOT NULL DEFAULT 1 CHECK(context_version >= 1),
 created_at TEXT NOT NULL,
 revoked_at TEXT
);
CREATE TABLE identity_operations (
 id TEXT PRIMARY KEY,
 browser_session_id TEXT NOT NULL REFERENCES browser_sessions(id),
 operation_type TEXT NOT NULL,
 input_hash TEXT NOT NULL,
 result_id TEXT NOT NULL,
 context_version INTEGER NOT NULL
);
CREATE TABLE deleted_identities (id TEXT PRIMARY KEY);
