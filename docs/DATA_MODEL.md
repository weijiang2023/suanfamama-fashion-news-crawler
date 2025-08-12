# Data Model · RunwayBase Agent

This document describes logical and physical data models for articles and related entities.

## Logical schema
- `sources`
  - id (string)
  - name (string)
  - type (enum)
  - homepageUrl, rssUrl?, sitemapUrl?, robotsTxtUrl?
  - crawlStrategy (enum)
  - active (bool)
  - crawlIntervalMinutes (int)
  - lastSuccessAt (timestamptz), lastError (text)
  - country?, languageDefault?
- `articles`
  - id (uuid/ksuid)
  - sourceId (fk)
  - canonicalUrl (text), urlHash (bytea)
  - title (text), authors (text[])
  - publishedAt (timestamptz), fetchedAt (timestamptz)
  - language (text)
  - bodyHtml (text), bodyText (text)
  - leadImageUrl (text), imageAttribution (text)
  - wordCount (int), summary (text)
  - createdAt, updatedAt
- `article_entities`
  - articleId (fk)
  - entityType (enum: brand|designer|location|event|person)
  - value (text)
  - confidence (float)
  - spanStart?, spanEnd?
- `article_categories`
  - articleId (fk)
  - category (enum)
  - confidence (float)
- `article_media`
  - id (uuid)
  - articleId (fk)
  - mediaType (enum: image|video)
  - url (text), caption (text), width?, height?, rights?

## PostgreSQL DDL (starter)
```sql
create table if not exists sources (
  id text primary key,
  name text not null,
  type text not null,
  homepage_url text not null,
  rss_url text,
  sitemap_url text,
  robots_txt_url text,
  crawl_strategy text not null,
  active boolean default true,
  crawl_interval_minutes int not null default 15,
  last_success_at timestamptz,
  last_error text,
  country text,
  language_default text
);

create table if not exists articles (
  id text primary key,
  source_id text not null references sources(id),
  canonical_url text not null,
  url_hash bytea not null,
  title text not null,
  authors text[] default '{}',
  published_at timestamptz,
  fetched_at timestamptz not null,
  language text,
  body_html text,
  body_text text,
  lead_image_url text,
  image_attribution text,
  word_count int,
  summary text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_articles_source_published on articles(source_id, published_at desc);
create unique index if not exists idx_articles_url_hash on articles(url_hash);

create table if not exists article_entities (
  article_id text not null references articles(id),
  entity_type text not null,
  value text not null,
  confidence real not null,
  span_start int,
  span_end int
);

create index if not exists idx_article_entities_article on article_entities(article_id);
create index if not exists idx_article_entities_value on article_entities(value);

create table if not exists article_categories (
  article_id text not null references articles(id),
  category text not null,
  confidence real not null
);

create index if not exists idx_article_categories_article on article_categories(article_id);

create table if not exists article_media (
  id text primary key,
  article_id text not null references articles(id),
  media_type text not null,
  url text not null,
  caption text,
  width int,
  height int,
  rights text
);
```

## OpenSearch mapping (starter)
```json
{
  "settings": {
    "index": {"number_of_shards": 1, "number_of_replicas": 0},
    "analysis": {
      "analyzer": {"default": {"type": "standard"}}
    }
  },
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
      "bodyText": {"type": "text"},
      "brands": {"type": "keyword"},
      "designers": {"type": "keyword"},
      "categories": {"type": "keyword"},
      "sourceName": {"type": "keyword"},
      "language": {"type": "keyword"},
      "publishedAt": {"type": "date"},
      "keywords": {"type": "keyword"},
      "summary": {"type": "text"}
    }
  }
}
```