# suanfamama-fashion-news-crawler

A simple Python crawler that aggregates top fashion news from curated RSS feeds and extracts full article content into a SQLite database.

## Quickstart

1. Install dependencies:

```bash
pip install -r /workspace/requirements.txt
```

2. Run the crawler (database will be created if missing):

```bash
python /workspace/main.py --db /workspace/data/articles.db --since-days 7 --max-per-feed 20
```

Optional: restrict to specific sources by name contains match:

```bash
python /workspace/main.py --only-sources "WWD" "The Cut"
```

Data is stored in the `articles` table with columns: `url`, `title`, `author`, `summary`, `content`, `top_image`, `published_at`, `source`, `category`, `fetched_at`.
