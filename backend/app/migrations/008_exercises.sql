-- Rebuild only this table to widen the original CHECK constraints.
-- The migration runner disables FK enforcement outside the transaction,
-- preserves all columns and verifies all foreign keys before committing.
CREATE TABLE exercise_sessions_new (
    id TEXT PRIMARY KEY,
    demo_user_id TEXT NOT NULL REFERENCES demo_users(id),
    skill_key TEXT NOT NULL CHECK(skill_key IN ('paced_breathing_4_6','sensory_grounding_5_4_3_2_1','stop','cognitive_reframe')),
    status TEXT NOT NULL CHECK(status IN ('in_progress','completed','stopped','interrupted')),
    started_at TEXT NOT NULL,
    ended_at TEXT,
    active_duration_ms INTEGER NOT NULL DEFAULT 0 CHECK(active_duration_ms BETWEEN 0 AND CASE WHEN skill_key='sensory_grounding_5_4_3_2_1' THEN 75000 ELSE 60000 END),
    paused_duration_ms INTEGER NOT NULL DEFAULT 0 CHECK(paused_duration_ms >= 0),
    last_checkpoint_at TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
    is_fixture INTEGER NOT NULL DEFAULT 0 CHECK(is_fixture IN (0,1)),
    owner_token TEXT
);
INSERT INTO exercise_sessions_new SELECT id,demo_user_id,skill_key,status,started_at,ended_at,active_duration_ms,paused_duration_ms,last_checkpoint_at,revision,is_fixture,owner_token FROM exercise_sessions;
DROP TABLE exercise_sessions;
ALTER TABLE exercise_sessions_new RENAME TO exercise_sessions;
