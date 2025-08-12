# suanfamama-fashion-news-crawler

A simple Python crawler that aggregates top fashion news from curated RSS feeds, extracts full article content, and stores it in a SQLite database. It also includes a minimal Flask UI to browse, search, and filter the articles.

## Features
- RSS aggregation from top fashion sources (see `app/sources.py`)
- Content extraction with BeautifulSoup + html5lib (pure Python, no compiled deps)
- SQLite storage with de-duplication by `url`
- CLI for crawling with source filtering and recency window
- Flask web UI with keyword search, source/category filters, pagination, and article detail view

## Project structure
```
/workspace
├── app/
│   ├── crawler.py        # Feed parsing + article extraction
│   ├── db.py             # SQLite schema + helpers
│   ├── sources.py        # Curated RSS sources
│   └── web.py            # Flask UI server
├── templates/
│   ├── base.html
│   ├── index.html        # Articles list + filters
│   └── article.html      # Article detail page
├── data/
│   └── articles.db       # SQLite database (created on first run)
├── main.py               # CLI entrypoint for crawling
└── requirements.txt
```

## Setup
Install dependencies (PEP 668 environments require the override flag):
```bash
pip install --break-system-packages -r /workspace/requirements.txt
```

## Usage
### 1) Crawl articles
Create or update the database with fresh articles:
```bash
python3 /workspace/main.py --db /workspace/data/articles.db --since-days 7 --max-per-feed 20
```
- **Limit sources**:
```bash
python3 /workspace/main.py --only-sources "WWD" "The Cut"
```
- Common flags:
  - `--db`: SQLite file path (default `/workspace/data/articles.db`)
  - `--since-days`: only include items within N days (if feed provides dates)
  - `--max-per-feed`: max items per feed to fetch
  - `--timeout`: request timeout for article pages

### 2) Launch the web UI
Start the Flask server to browse the stored articles:
```bash
python3 /workspace/app/web.py --db /workspace/data/articles.db --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

- Filters: keyword (`q`), `source`, `category`, `days`, `per_page`
- Sorting: newest first by `published_at` (when available), then `fetched_at`

## Customization
- Edit or extend sources in `app/sources.py` (add/remove feeds, adjust categories)
- Adjust extraction logic in `app/crawler.py` (e.g., selectors for title/image/content)
- Change schema or indices in `app/db.py` as needed

## Scheduling (optional)
Run the crawler periodically with cron/systemd. Example cron (hourly):
```cron
0 * * * * python3 /workspace/main.py --db /workspace/data/articles.db --since-days 7 --max-per-feed 30 --timeout 15 >> /workspace/crawl.log 2>&1
```

## Troubleshooting
- "externally-managed-environment" from pip: use `--break-system-packages` as shown above.
- `python: command not found`: use `python3`.
- Network timeouts: increase `--timeout` or reduce `--max-per-feed`.
- Empty images: not all sites expose `og:image`; thumbnails appear when present.

## License
MIT (add your preferred license if different)
