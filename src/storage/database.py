# src/storage/database.py

import sqlite3
import logging
from typing import List, Dict
import os

DB_PATH = "data/news_papers.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # News Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            source TEXT,
            published_at TEXT,
            summary TEXT,
            diagram TEXT,
            score REAL
        )
    """)

    # Papers Table
    c.execute("""
               CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            arxiv_id TEXT,
            published TEXT,
            authors TEXT,
            summary TEXT,
            diagram TEXT,
            insights TEXT,
            score REAL
        )

    """)
    # Create or update papers table
    c.execute("PRAGMA table_info(papers)")
    columns = [col[1] for col in c.fetchall()]
    if "insights" not in columns:
        c.execute("ALTER TABLE papers ADD COLUMN insights TEXT")
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def save_to_db(content_type: str, items: List[Dict]):
    """
    Save ranked news or papers to SQLite database.

    Args:
        content_type (str): 'news' or 'papers'
        items (List[Dict]): List of dicts with fields to save
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        if content_type == "news":
            for item in items:
                c.execute("""
                    INSERT OR IGNORE INTO news (title, url, source, published_at, summary, diagram, score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.get("title"),
                    item.get("url"),
                    item.get("source"),
                    item.get("published_at"),
                    item.get("summary"),
                    item.get("diagram", ""),
                    item.get("score", 0.0)
                ))

        elif content_type == "papers":
            for item in items:
                c.execute("""
    INSERT OR IGNORE INTO papers (title, link, arxiv_id, published, authors, summary, diagram, insights, score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
                    item.get("title"),
                    item.get("link"),
                    item.get("arxiv_id"),
                    item.get("published"),
                    ", ".join(item.get("authors", [])),
                    item.get("summary"),
                    item.get("diagram", ""),
                    str(item.get("insights", {})),  # store as stringified dict
                    item.get("score", 0.0)
                ))


        else:
            logging.warning(f"Unsupported content type: {content_type}")
            return

        conn.commit()
        logging.info(f"{len(items)} {content_type} entries saved to DB.")

    except Exception as e:
        logging.error(f"Failed to save to DB: {e}")

    finally:
        conn.close()
