import os
from datetime import datetime

import sqlite3
import pytest

from app.db import init_db, get_db, insert_article, bulk_insert_articles


def test_init_db_creates_schema(tmp_path):
    db_path = tmp_path / "articles.db"
    init_db(str(db_path))

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
        row = cur.fetchone()
        assert row is not None


def test_insert_and_bulk_insert_with_dedup(tmp_path):
    db_path = tmp_path / "articles.db"
    init_db(str(db_path))

    article = {
        "url": "https://example.com/a1",
        "title": "Title 1",
        "author": "Author",
        "summary": "Summary",
        "content": "Content " * 50,
        "top_image": None,
        "published_at": datetime.utcnow().isoformat(),
        "source": "Test Source",
        "category": "general",
    }

    with get_db(str(db_path)) as conn:
        # First insert should succeed
        ok = insert_article(conn, article)
        assert ok is True

        # Duplicate should be ignored
        ok2 = insert_article(conn, article)
        assert ok2 is False

        # Bulk insert should count only new
        more = [
            {**article, "url": "https://example.com/a2", "title": "T2"},
            {**article, "url": "https://example.com/a1", "title": "T1-dup"},  # duplicate
        ]
        count = bulk_insert_articles(conn, more)
        assert count == 1

        # Verify total rows = 2
        cur = conn.execute("SELECT COUNT(*) FROM articles")
        total = cur.fetchone()[0]
        assert total == 2