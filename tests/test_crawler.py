import types
from datetime import datetime, timedelta

import pytest

from app import crawler as crawler_mod


def test_normalize_url_strips_utm_params():
    url = "https://example.com/article?utm_source=foo&id=123&utm_medium=x#frag"
    assert crawler_mod.normalize_url(url) == "https://example.com/article?id=123#frag"


def test_parse_entry_datetime_handles_various_fields():
    now = datetime.utcnow()
    iso = now.isoformat()
    # dict with published
    entry = {"published": iso}
    assert crawler_mod.parse_entry_datetime(entry) == iso
    # attribute-based entry with updated
    entry2 = types.SimpleNamespace(updated=iso)
    assert crawler_mod.parse_entry_datetime(entry2) == iso


@pytest.mark.asyncio
async def test_crawl_feed_filters_old_and_requires_min_content(monkeypatch):
    # Build two entries: one recent, one old
    recent_dt = datetime.utcnow().isoformat()
    old_dt = (datetime.utcnow() - timedelta(days=365)).isoformat()

    entries = [
        {"link": "https://example.com/recent", "title": "Recent", "author": "A", "summary": "S", "published": recent_dt},
        {"link": "https://example.com/old", "title": "Old", "author": "B", "summary": "S", "published": old_dt},
    ]

    class MockParsed:
        def __init__(self, entries):
            self.entries = entries

    def mock_feedparser_parse(url, request_headers=None):
        assert "http" in url
        return MockParsed(entries)

    class MockResponse:
        def __init__(self, text: str, status_code: int = 200):
            self.text = text
            self.status_code = status_code

    def mock_requests_get(url, headers=None, timeout=None):
        if "recent" in url:
            # Make content > 200 chars, include og:image
            big_para = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 6
            html = f"""
            <html><head><meta property='og:image' content='https://img.example.com/one.jpg' /></head>
            <body><article><p>{big_para}</p><p>More text here to cross threshold.</p></article></body></html>
            """
            return MockResponse(html)
        # Old article shouldn't be fetched ideally, but crawl_feed may still attempt before filtering by date
        return MockResponse("<html><body><article><p>short</p></article></body></html>")

    monkeypatch.setattr(crawler_mod.feedparser, "parse", mock_feedparser_parse)
    monkeypatch.setattr(crawler_mod.requests, "get", mock_requests_get)

    feed = {"name": "Test Feed", "url": "https://feed.example.com/rss", "category": "general"}
    items = crawler_mod.crawl_feed(feed, max_per_feed=10, since_days=30, request_timeout=5)

    # Should include only the recent item and only if content len >= 200
    assert len(items) == 1
    item = items[0]
    assert item["url"] == "https://example.com/recent"
    assert item["title"] == "Recent"
    assert item["author"] == "A"
    assert item["summary"] == "S"
    assert item["top_image"] == "https://img.example.com/one.jpg"
    assert item["published_at"] is not None
    assert item["source"] == "Test Feed"
    assert item["category"] == "general"