CREATE TABLE IF NOT EXISTS preferences (
 owner_id TEXT PRIMARY KEY REFERENCES demo_users(id) ON DELETE CASCADE,
 revision INTEGER NOT NULL,
 answers TEXT
);
CREATE TABLE IF NOT EXISTS preference_operations (
 owner_id TEXT NOT NULL REFERENCES demo_users(id) ON DELETE CASCADE,
 operation_id TEXT NOT NULL,
 fingerprint TEXT NOT NULL,
 PRIMARY KEY(owner_id,operation_id)
);
