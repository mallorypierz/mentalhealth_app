CREATE TABLE voice_provider_attempts (
 id TEXT PRIMARY KEY,
 operation_key TEXT NOT NULL UNIQUE,
 stage TEXT NOT NULL,
 reserved_microdollars INTEGER NOT NULL CHECK(reserved_microdollars > 0),
 outcome TEXT NOT NULL DEFAULT 'reserved',
 created_at TEXT NOT NULL
);
