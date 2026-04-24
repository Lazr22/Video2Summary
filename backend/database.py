import sqlite3
import time
import json

DB_PATH = "video2summary.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            transcript TEXT,
            summary TEXT,
            language TEXT,
            duration REAL,
            word_count INTEGER,
            created_at REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result_id INTEGER NOT NULL,
            question TEXT,
            answer TEXT,
            created_at REAL,
            FOREIGN KEY (result_id) REFERENCES results(id)
        )
    """)
    conn.commit()
    conn.close()


def save_result(filename, transcript, summary, language, duration, word_count):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO results (filename, transcript, summary, language, duration, word_count, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (filename, transcript, summary, language, duration, word_count, time.time()),
    )
    record_id = c.lastrowid
    conn.commit()
    conn.close()
    return record_id


def save_questions(result_id, pairs):
    """Save a list of {question, answer} dicts for a result."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Delete any previously generated questions for this result
    c.execute("DELETE FROM questions WHERE result_id = ?", (result_id,))
    ts = time.time()
    for pair in pairs:
        c.execute(
            "INSERT INTO questions (result_id, question, answer, created_at) VALUES (?, ?, ?, ?)",
            (result_id, pair["question"], pair["answer"], ts),
        )
    conn.commit()
    conn.close()


def get_questions(result_id):
    """Get saved Q&A pairs for a result. Returns [] if none yet."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT question, answer FROM questions WHERE result_id = ? ORDER BY id",
        (result_id,)
    )
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM results ORDER BY created_at DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def get_record(record_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM results WHERE id = ?", (record_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
