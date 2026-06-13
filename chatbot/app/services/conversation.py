"""Persistencia de conversaciones (SQLite)."""
from __future__ import annotations

import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Iterator

from ..config import get_settings

_lock = threading.Lock()
_initialized = False


SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    channel       TEXT    NOT NULL,
    user_id       TEXT    NOT NULL,
    role          TEXT    NOT NULL,           -- 'user' | 'assistant'
    content       TEXT    NOT NULL,
    created_at    REAL    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_messages_user
    ON messages(channel, user_id, created_at);

CREATE TABLE IF NOT EXISTS processed (
    message_id    TEXT PRIMARY KEY,
    created_at    REAL NOT NULL
);
"""


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    s = get_settings()
    c = sqlite3.connect(s.conversations_db)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init_db() -> None:
    global _initialized
    with _lock:
        if _initialized:
            return
        with _conn() as c:
            c.executescript(SCHEMA)
        _initialized = True


def already_processed(message_id: str) -> bool:
    with _conn() as c:
        row = c.execute(
            "SELECT 1 FROM processed WHERE message_id = ?", (message_id,)
        ).fetchone()
        if row:
            return True
        c.execute(
            "INSERT INTO processed(message_id, created_at) VALUES (?, ?)",
            (message_id, time.time()),
        )
        return False


def append_message(channel: str, user_id: str, role: str, content: str) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO messages(channel, user_id, role, content, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (channel, user_id, role, content, time.time()),
        )


def get_history(channel: str, user_id: str, limit: int = 20) -> list[dict]:
    """Últimos `limit` mensajes en orden cronológico."""
    with _conn() as c:
        rows = c.execute(
            "SELECT role, content FROM messages "
            "WHERE channel = ? AND user_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (channel, user_id, limit),
        ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
