import argparse
import os
from typing import List, Dict, Any

from app.db import init_db, get_db, bulk_insert_articles
from app.sources import RSS_SOURCES
from app.crawler import crawl_all


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl top fashion news into a SQLite database")
    parser.add_argument("--db", default="/workspace/data/articles.db", help="Path to SQLite database file")
    parser.add_argument("--since-days", type=int, default=7, help="Only include items published within the last N days (if date available)")
    parser.add_argument("--max-per-feed", type=int, default=20, help="Maximum number of items to pull per feed")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds for article fetching")
    parser.add_argument("--only-sources", nargs="*", default=None, help="Optional list of source names to include (match by name contains)")
    return parser.parse_args()


def filter_sources(sources: List[Dict[str, str]], only: List[str] | None) -> List[Dict[str, str]]:
    if not only:
        return sources
    lowered = [o.lower() for o in only]
    return [s for s in sources if any(o in s["name"].lower() for o in lowered)]


def main() -> None:
    args = parse_args()
    init_db(args.db)

    selected_sources = filter_sources(RSS_SOURCES, args.only_sources)
    articles: List[Dict[str, Any]] = crawl_all(
        feeds=selected_sources,
        max_per_feed=args.max_per_feed,
        since_days=args.since_days,
        request_timeout=args.timeout,
    )

    with get_db(args.db) as connection:
        inserted = bulk_insert_articles(connection, articles)

    print(f"Fetched {len(articles)} articles; inserted {inserted} new into {args.db}")


if __name__ == "__main__":
    main()