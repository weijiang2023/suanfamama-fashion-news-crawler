# Architecture: RunwayBase Agent

Last updated: 2025-08-12

## TL;DR
RunwayBase Agent ingests fashion news from prioritized sources, enriches the content with a vertical domain knowledgebase (brands, designers, seasons, shows), and exposes a low-latency search API. The system is built as a resilient, horizontally scalable pipeline with strong compliance to robots.txt and source TOS.

## High-level Architecture
```mermaid
graph LR
  subgraph Ingestion
    SCH[Scheduler]
    Q[Queue (Redis Streams)]
    F1[HTTP Fetcher Workers]
    F2[JS Fetcher Workers (Playwright)]
    P[Parser]
    N[Normalizer]
    D[Deduper]
    E[Enrichment]
    IX[Index Writer]
  end

  subgraph Storage & Indexes
    PG[(PostgreSQL: metadata)]
    S3[(Object Storage: raw HTML, screenshots)]
    OS[(OpenSearch: search index)]
  end

  subgraph Control Plane
    ADM[Admin/API]
    SR[Source Registry]
    MON[Monitoring]
  end

  SCH --> Q
  ADM --> SR
  SR --> SCH
  Q --> F1
  Q --> F2
  F1 --> P
  F2 --> P
  P --> N --> D --> E --> IX
  P --> S3
  IX --> OS
  E --> PG
  D --> PG
  N --> PG
  ADM --> PG
  ADM --> OS
  MON --> ADM
  MON --> Ingestion
```

## Data Flow (happy path)
1. Scheduler reads active sources and schedules crawl jobs into the queue respecting per-domain rate limits and robots.txt.
2. Fetchers pull jobs: HTTP-first; JS-rendered via Playwright for sites requiring client-side rendering.
3. Parser extracts structured fields (title, author, date, body, media, canonical) using a hybrid approach: boilerplate removal (Readability) + per-source CSS/XPath selectors.
4. Normalizer cleans HTML, resolves links, converts timezones, and standardizes fields.
5. Deduper computes hashes and clusters near-duplicates using canonical URL + content shingling.
6. Enrichment runs entity extraction (brands, designers, locations, events), category classification, summarization, and runway/show schema detection.
7. Index Writer persists to PostgreSQL and OpenSearch; raw HTML and screenshots stored in object storage.
8. Admin/API exposes search/read endpoints and operational dashboards.

## Components
- Scheduler
  - Cron-like orchestrator that enqueues jobs per source with jitter and backoff.
  - Respects `crawlIntervalMinutes`, last success/failure, and per-domain concurrency.
- Source Registry
  - Defines source metadata, crawl strategy (RSS, sitemap, HTML, JS), selectors, and compliance notes.
- Fetchers
  - HTTP fetcher with retry policy (exponential backoff, circuit breaker, proxy pool if needed).
  - JS fetcher via Playwright with headless browser pool and resource blocking.
  - Politeness: custom user-agent, robots parser, per-host rate limiter.
- Parser
  - Boilerplate removal + per-source selectors; fallbacks if selectors fail.
  - Media extraction with attribution when available.
- Normalizer
  - Unicode normalization, HTML sanitization, absolute URL resolution, timezone handling.
- Deduper
  - URL hash and content MinHash/shingles for near-duplicate clustering.
- Enrichment
  - NER using domain-adapted models and a curated brand/designer gazetteer.
  - Category classifier for fashion domains; 2–3 sentence summarizer; keyword extractor.
  - Runway/show schema detection: brand, season, city, collection name.
- Index Writer
  - Upserts records to PostgreSQL; writes denormalized documents to OpenSearch with analyzers.
- Admin/API Service
  - REST API for articles, trends, and sources; admin views for health and QA.
- Storage & Indexes
  - PostgreSQL for metadata; OpenSearch for query; S3-compatible for raw assets.
- Observability
  - Prometheus metrics, Loki/ELK logs, Sentry errors; Grafana dashboards.

## Deployment
- Containerized services (Docker); recommended orchestration via Kubernetes.
- Suggested pods/services:
  - api (FastAPI) | replicas 2–4
  - admin (if separate) | replicas 1–2
  - scheduler | 1
  - worker-http | HPA on Q depth
  - worker-js | HPA on Q depth (lower ceilings)
  - indexer | 1–2
- Datastores (managed where possible): PostgreSQL, OpenSearch, Redis, S3-compatible.
- Autoscaling signals: queue depth, fetch latency, error rate, CPU for JS workers.
- Secrets: mounted from a vault; never in env/plaintext.
- Network egress: respect source geo; optional proxy pool with allowlist.

## Compliance & Politeness
- Parse and honor robots.txt; skip disallowed paths.
- Identify as RunwayBase Agent in user-agent; provide contact URL.
- Per-host rate limits and concurrency caps; exponential backoff on 4xx/5xx.
- Do not bypass paywalls or protected content; do not log PII.

## Search Index Design (OpenSearch)
- Index: `articles_v1` with fields: id, title, bodyText, brands, designers, categories, source, language, publishedAt, keywords, summary, entities.
- Analyzers: language-specific analyzers per `language`; keyword fields for facets.
- Mappings tuned for facet aggregations and time histograms.

## Monitoring & Alerting
- Key metrics: ingestion latency, error rates by source, dedup ratio, enrichment precision samples, queue depth, API p95 latency.
- Alerts: source failure >30m, index lag >60m, API 5xx >1%/5m, Playwright failure surge, crawl ban signals.

## Data Retention & Backups
- PostgreSQL: daily snapshots + PITR.
- OpenSearch: snapshot to object storage.
- Raw HTML/screenshots: 30–90 days rolling (configurable) with lifecycle policies.

## Security
- API keys in header `X-API-Key`; per-tenant keys optional in v1.
- RBAC for admin; IP allowlist for admin UI.
- Audit logs for admin actions.

## Failure Modes & Recovery
- Poison messages: move to dead-letter stream with sample stored for QA.
- Selector drift: automatic fallback + alert; admin override to hotfix selectors.
- JS-render instability: cap concurrency; retry with HTTP-only path; temporary pause source.

## Local Development
- Dev compose file running API, workers, Postgres, OpenSearch, Redis, MinIO.
- Seed sample sources and golden dataset for QA.