CREATE TABLE IF NOT EXISTS conversations (
 id TEXT PRIMARY KEY,
 demo_user_id TEXT NOT NULL REFERENCES demo_users(id),
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS requests (
 id TEXT PRIMARY KEY,
 conversation_id TEXT NOT NULL REFERENCES conversations(id),
 input_hash TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('pending','succeeded','failed')),
 attempt_count INTEGER NOT NULL DEFAULT 1,
 provider_call_count INTEGER NOT NULL DEFAULT 0,
 mock_mode TEXT NOT NULL CHECK(mock_mode IN ('success','failure','delayed')),
 error_code TEXT,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS one_pending_request ON requests(conversation_id) WHERE status='pending';
CREATE TABLE IF NOT EXISTS messages (
 id TEXT PRIMARY KEY,
 conversation_id TEXT NOT NULL REFERENCES conversations(id),
 request_id TEXT NOT NULL REFERENCES requests(id),
 role TEXT NOT NULL CHECK(role IN ('user','assistant')),
 content TEXT NOT NULL,
 sequence INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 UNIQUE(conversation_id, sequence),
 UNIQUE(request_id, role)
);
CREATE TABLE IF NOT EXISTS conversation_operations (
 id TEXT PRIMARY KEY,
 demo_user_id TEXT NOT NULL REFERENCES demo_users(id),
 operation_type TEXT NOT NULL,
 target_id TEXT NOT NULL,
 input_hash TEXT NOT NULL
);
