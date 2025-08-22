import sqlite3
import json
from typing import Dict

DB_NAME = "gaming_ai.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        analysis TEXT,
        tips TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    conn.commit()
    conn.close()

def save_analysis(user_id: str, analysis: Dict, tips: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO analyses (user_id, analysis, tips) VALUES (?, ?, ?)",
        (user_id, json.dumps(analysis), tips),
    )
    conn.commit()
    conn.close()