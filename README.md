# suanfamama-fashion-news-crawler

A simple Python crawler that aggregates top fashion news from curated RSS feeds and extracts full article content into a SQLite database.

## Quickstart

1. Install dependencies:

```bash
pip install --break-system-packages -r /workspace/requirements.txt
```

2. Run the crawler (database will be created if missing):

```bash
python3 /workspace/main.py --db /workspace/data/articles.db --since-days 7 --max-per-feed 20
```

Optional: restrict to specific sources by name contains match:

```bash
python3 /workspace/main.py --only-sources "WWD" "The Cut"
```

3. Launch the web UI:

```bash
python3 /workspace/app/web.py --db /workspace/data/articles.db --port 8000
```

Then open http://localhost:8000 in your browser.

Data is stored in the `articles` table with columns: `url`, `title`, `author`, `summary`, `content`, `top_image`, `published_at`, `source`, `category`, `fetched_at`.
