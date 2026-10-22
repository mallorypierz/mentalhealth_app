CREATE TABLE IF NOT EXISTS provider_attempts (
 id TEXT PRIMARY KEY,
 request_id TEXT NOT NULL REFERENCES requests(id),
 attempt INTEGER NOT NULL,
 stage TEXT NOT NULL CHECK(stage IN ('planning','answer')),
 provider TEXT NOT NULL,
 model TEXT NOT NULL,
 outcome TEXT NOT NULL DEFAULT 'reserved',
 input_tokens INTEGER,
 output_tokens INTEGER,
 created_at TEXT NOT NULL,
 UNIQUE(request_id,attempt,stage)
);
