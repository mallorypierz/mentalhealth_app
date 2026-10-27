CREATE TABLE voice_sessions (
 id TEXT PRIMARY KEY,
 conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
 browser_session_id TEXT NOT NULL REFERENCES browser_sessions(id),
 context_version INTEGER NOT NULL,
 state TEXT NOT NULL CHECK(state IN ('ready','active','stopped','interrupted')),
 revision INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE UNIQUE INDEX one_voice_session ON voice_sessions(conversation_id) WHERE state IN ('ready','active');
CREATE TABLE voice_turns (
 id TEXT PRIMARY KEY,
 session_id TEXT NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
 sequence INTEGER NOT NULL,
 reserved_request_id TEXT NOT NULL UNIQUE,
 request_id TEXT UNIQUE REFERENCES requests(id),
 transcription TEXT NOT NULL DEFAULT 'pending',
 submission TEXT NOT NULL DEFAULT 'not_saved',
 speech TEXT NOT NULL DEFAULT 'not_started',
 state TEXT NOT NULL DEFAULT 'processing',
 error_code TEXT,
 revision INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 UNIQUE(session_id,sequence)
);
CREATE UNIQUE INDEX one_voice_turn ON voice_turns(session_id) WHERE state='processing';
CREATE TABLE voice_operations (
 id TEXT PRIMARY KEY,
 session_id TEXT NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
 target_id TEXT NOT NULL,
 action TEXT NOT NULL,
 input_hash TEXT NOT NULL
);
