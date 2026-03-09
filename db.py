import sqlite3
from pathlib import Path

from config import DB_PATH
from schema import CREATE_TABLE_EVENTS


def get_connection():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(CREATE_TABLE_EVENTS)


def event_exists(conn: sqlite3.Connection, user_id: int, channel_id: int, event_type: str, timestamp: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM events WHERE user_id=? AND channel_id=? AND event_type=? AND timestamp=? LIMIT 1",
        (user_id, channel_id, event_type, timestamp),
    ).fetchone()

    return row is not None


def insert_event(conn: sqlite3.Connection, user_id: int, username: str | None, channel_id: int, event_type: str, timestamp: str):
    conn.execute(
        "INSERT INTO events (user_id, username, channel_id, event_type, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, channel_id, event_type, timestamp),
    )
