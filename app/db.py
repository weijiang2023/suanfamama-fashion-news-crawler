import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Any, Iterable


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    title TEXT,
    author TEXT,
    summary TEXT,
    content TEXT,
    top_image TEXT,
    published_at TEXT,
    source TEXT,
    category TEXT,
    fetched_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
"""


def ensure_parent_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def init_db(db_path: str) -> None:
    ensure_parent_dir(db_path)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA_SQL)
        connection.commit()


@contextmanager
def get_db(db_path: str):
    connection = sqlite3.connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


def insert_article(connection: sqlite3.Connection, article: Dict[str, Any]) -> bool:
    sql = (
        "INSERT OR IGNORE INTO articles (url, title, author, summary, content, top_image, "
        "published_at, source, category, fetched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    values = (
        article.get("url"),
        article.get("title"),
        article.get("author"),
        article.get("summary"),
        article.get("content"),
        article.get("top_image"),
        article.get("published_at"),
        article.get("source"),
        article.get("category"),
        datetime.utcnow().isoformat(),
    )
    cursor = connection.cursor()
    cursor.execute(sql, values)
    connection.commit()
    return cursor.rowcount == 1


def bulk_insert_articles(connection: sqlite3.Connection, articles: Iterable[Dict[str, Any]]) -> int:
    inserted = 0
    for article in articles:
        try:
            if insert_article(connection, article):
                inserted += 1
        except sqlite3.Error:
            # Continue on individual failures to avoid aborting the whole batch
            continue
    return inserted