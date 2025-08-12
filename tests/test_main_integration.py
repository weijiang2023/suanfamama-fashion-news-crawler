import builtins
from contextlib import nullcontext
from types import SimpleNamespace

import main as main_module


def test_main_happy_path(monkeypatch, capsys, tmp_path):
    # Mock args
    args = SimpleNamespace(
        db=str(tmp_path / "articles.db"),
        since_days=7,
        max_per_feed=5,
        timeout=10,
        only_sources=None,
    )
    monkeypatch.setattr(main_module, "parse_args", lambda: args)

    # Mock DB functions
    inserted_counter = {"count": 0}

    def fake_init_db(db_path):
        return None

    class FakeConn:
        pass

    class FakeCtx:
        def __init__(self, conn):
            self.conn = conn

        def __enter__(self):
            return self.conn

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_get_db(db_path):
        return FakeCtx(FakeConn())

    def fake_bulk_insert(conn, articles):
        inserted_counter["count"] = len(articles)
        return len(articles)

    monkeypatch.setattr(main_module, "init_db", fake_init_db)
    monkeypatch.setattr(main_module, "get_db", fake_get_db)
    monkeypatch.setattr(main_module, "bulk_insert_articles", fake_bulk_insert)

    # Mock sources and crawler to return two articles
    monkeypatch.setattr(main_module, "RSS_SOURCES", [
        {"name": "S1", "url": "https://s1", "category": "general"},
        {"name": "S2", "url": "https://s2", "category": "general"},
    ])

    def fake_crawl_all(feeds, max_per_feed, since_days, request_timeout):
        assert len(feeds) == 2
        return [
            {"url": "u1", "title": "t1", "author": None, "summary": None, "content": "x" * 300, "top_image": None, "published_at": None, "source": "S1", "category": "general"},
            {"url": "u2", "title": "t2", "author": None, "summary": None, "content": "y" * 300, "top_image": None, "published_at": None, "source": "S2", "category": "general"},
        ]

    monkeypatch.setattr(main_module, "crawl_all", fake_crawl_all)

    main_module.main()

    captured = capsys.readouterr().out
    assert "Fetched 2 articles; inserted 2 new" in captured
    assert inserted_counter["count"] == 2