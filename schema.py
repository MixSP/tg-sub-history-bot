CREATE_TABLE_EVENTS = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    channel_id INTEGER NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('joined', 'left')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, channel_id, event_type, timestamp)
);
"""
