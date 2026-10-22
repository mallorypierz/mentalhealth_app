-- Initial save/read increment only; later tables require separate migrations.
CREATE TABLE IF NOT EXISTS demo_users (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS exercise_sessions (
    id TEXT PRIMARY KEY,
    demo_user_id TEXT NOT NULL REFERENCES demo_users(id),
    skill_key TEXT NOT NULL CHECK(skill_key = 'paced_breathing_4_6'),
    status TEXT NOT NULL CHECK(status IN ('in_progress','completed','stopped','interrupted')),
    started_at TEXT NOT NULL,
    ended_at TEXT,
    active_duration_ms INTEGER NOT NULL DEFAULT 0 CHECK(active_duration_ms BETWEEN 0 AND 60000),
    paused_duration_ms INTEGER NOT NULL DEFAULT 0 CHECK(paused_duration_ms >= 0),
    last_checkpoint_at TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
    is_fixture INTEGER NOT NULL DEFAULT 0 CHECK(is_fixture IN (0,1))
);
CREATE TABLE IF NOT EXISTS operations (
    id TEXT PRIMARY KEY,
    demo_user_id TEXT NOT NULL REFERENCES demo_users(id),
    operation_type TEXT NOT NULL,
    target_id TEXT NOT NULL REFERENCES exercise_sessions(id),
    input_hash TEXT NOT NULL,
    result_json TEXT NOT NULL
);
