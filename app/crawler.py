import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from tqdm import tqdm

DEFAULT_HEADERS = {
    "User-Agent": "FashionNewsCrawler/1.0 (+https://example.com; contact@example.com)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def normalize_url(url: str) -> str:
    # Light URL normalization; avoid losing canonicalization
    try:
        from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

        split = urlsplit(url)
        query_pairs = [(k, v) for k, v in parse_qsl(split.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
        normalized = urlunsplit((split.scheme, split.netloc, split.path, urlencode(query_pairs), split.fragment))
        return normalized
    except Exception:
        return url


def parse_entry_datetime(entry: Dict[str, Any]) -> Optional[str]:
    dt_candidates: List[Optional[str]] = [
        getattr(entry, "published", None),
        getattr(entry, "updated", None),
        entry.get("published"),
        entry.get("updated"),
        entry.get("pubDate"),
    ]
    for value in dt_candidates:
        if not value:
            continue
        try:
            dt = dateparser.parse(value)
            if dt:
                return dt.isoformat()
        except Exception:
            continue
    return None


def fetch_and_extract(url: str, timeout: int = 20) -> Dict[str, Optional[str]]:
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        if response.status_code >= 400 or not response.text:
            return {"content": None, "top_image": None}
        soup = BeautifulSoup(response.text, "html5lib")
        # Remove scripts/styles/navs and elements that usually are noise
        for selector in ["script", "style", "noscript", "header", "footer", "nav", "aside"]:
            for element in soup.select(selector):
                element.decompose()
        # Prefer article tag text, fallback to main, then body
        content_container = soup.find("article") or soup.find("main") or soup.body
        content_text = None
        if content_container:
            # Join paragraphs to form content text
            paragraphs = [p.get_text(separator=" ", strip=True) for p in content_container.find_all("p")]
            content_text = "\n\n".join([p for p in paragraphs if p])
        # Find og:image for top image
        og_image = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
        top_image = og_image["content"].strip() if og_image and og_image.get("content") else None
        return {"content": content_text, "top_image": top_image}
    except Exception:
        return {"content": None, "top_image": None}


def crawl_feed(feed: Dict[str, str], max_per_feed: int, since_days: int, request_timeout: int) -> List[Dict[str, Any]]:
    parsed = feedparser.parse(feed["url"], request_headers=DEFAULT_HEADERS)
    cutoff = datetime.utcnow() - timedelta(days=since_days)

    articles: List[Dict[str, Any]] = []
    for entry in parsed.entries[: max_per_feed or None]:
        link = normalize_url(getattr(entry, "link", None) or entry.get("link", ""))
        if not link:
            continue
        published_iso = parse_entry_datetime(entry)
        # Skip very old items if published date available and older than cutoff
        if published_iso:
            try:
                if dateparser.parse(published_iso) < cutoff:
                    continue
            except Exception:
                pass

        title = getattr(entry, "title", None) or entry.get("title")
        author = getattr(entry, "author", None) or entry.get("author")
        summary = getattr(entry, "summary", None) or entry.get("summary")

        extraction = fetch_and_extract(link, timeout=request_timeout)
        content = extraction.get("content")
        top_image = extraction.get("top_image")

        if content and len(content.strip()) >= 200:
            articles.append(
                {
                    "url": link,
                    "title": title,
                    "author": author,
                    "summary": summary,
                    "content": content,
                    "top_image": top_image,
                    "published_at": published_iso,
                    "source": feed.get("name"),
                    "category": feed.get("category"),
                }
            )
    return articles


def crawl_all(feeds: List[Dict[str, str]], max_per_feed: int = 30, since_days: int = 7, request_timeout: int = 20) -> List[Dict[str, Any]]:
    all_articles: List[Dict[str, Any]] = []
    for feed in tqdm(feeds, desc="Feeds", unit="feed"):
        try:
            items = crawl_feed(feed, max_per_feed=max_per_feed, since_days=since_days, request_timeout=request_timeout)
            all_articles.extend(items)
        except Exception as exc:
            logging.warning("Failed to crawl feed %s: %s", feed.get("name"), exc)
            continue
        # Be polite between different sites
        time.sleep(0.5)
    return all_articles