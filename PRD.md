## Product Requirements Document (PRD)

### Product: suanfamama-fashion-news-crawler
### Doc Owner: PM/Tech Lead
### Status: Draft v0.1
### Last Updated: 2025-08-12

---

## 1. Overview
- **Problem**: Fashion professionals and enthusiasts lack a centralized, timely, and structured feed of fashion news across brands, magazines, retailers, and events. Information is fragmented, inconsistent, and often locked in unstructured HTML.
- **Solution**: A compliant web crawling and content enrichment platform that discovers, normalizes, and indexes fashion news in near real time. Provides APIs and optional UI for search, filtering, and trend insights.
- **Outcome**: Faster research, better monitoring of brands/topics, and a structured dataset for analytics.

## 2. Goals and Non‑Goals
- **Goals**:
  - Aggregate fashion news from top sources with <30 min freshness (P95) for new posts.
  - Normalize articles (title, author, date, body, media, canonical URL) with >98% availability.
  - Enrich content with fashion taxonomy: brands, designers, seasons, shows, categories, locations.
  - Provide search and filter APIs with facets (brand, category, source, date, language).
  - Admin tools to manage sources, crawl schedules, and review extraction quality.
- **Non‑Goals** (initially):
  - Social media scraping requiring login or TOS‑restricted access.
  - Full editorial UI/CMS.
  - Real‑time user personalization or recommendations.
  - Paid content circumvention.

## 3. Target Users and Personas
- **Analyst**: Tracks brands, trends, sustainability reports. Needs alerts and export.
- **PR/Brand Manager**: Monitors coverage mentions, sentiment, competitor launches.
- **Editor/Curator**: Needs a clean feed to curate newsletters or site modules.
- **Data Scientist**: Consumes enriched dataset via API/warehouse for models.

## 4. Key Use Cases
- Track all news about “Gucci” in the last 24h with sentiment and top sources.
- Identify trending designers during Fashion Week by city and season.
- Export all runway reviews of “Louis Vuitton” FW24 across publications.
- API embed: show the latest 10 “Sustainability” articles on a site.

## 5. Scope (MVP → v1)
- **MVP (v0)**:
  - Crawl 30 priority sources (magazines, brand pressrooms, retailer blogs, wires).
  - Extraction of core fields; English only.
  - Basic enrichment: brand/designer/entity tags, category classification, summary.
  - REST API for list/search, facets, and article detail.
  - Source management in admin; basic health dashboards.
- **v1**:
  - 150+ sources, multi‑language (EN, FR, IT, ZH).
  - Runway/show metadata extraction (brand, season, city, collection name).
  - Image detection, caption extraction, and rights metadata.
  - Trend endpoints (top brands/topics) and newsletter export.

## 6. Functional Requirements
- **FR1 – Source Management**: CRUD sources, crawl method (RSS, sitemap, HTML, JS‑rendered), schedule, rules, auth headers if any, respect robots.txt.
- **FR2 – Discovery**: Detect new/updated articles via RSS/sitemaps and delta crawl.
- **FR3 – Fetching**: HTTP fetch with polite rate limits, retries, proxy pool, geo if needed.
- **FR4 – Parsing**: Auto and per‑source selectors to extract title, author, date, body, media, canonical, tags.
- **FR5 – Normalization**: Clean HTML to article text; resolve relative URLs; timezone normalization.
- **FR6 – Deduplication**: Canonical URL + content hash; cluster near‑duplicates.
- **FR7 – Enrichment**:
  - NER for brands, designers, people, locations, events.
  - Category classifier: {Runway, Trend, Retail, Celebrity, Business, Sustainability, Beauty, Street Style}.
  - Summarization (<= 3 sentences) and keyword extraction.
  - Runway/show schema detection (brand, season, city, collection).
- **FR8 – Indexing & Search**: Free‑text search, filters, sort by date/relevance; facets for brand, category, source, language, date histogram.
- **FR9 – API**: Authenticated REST endpoints for search and retrieval (see §9).
- **FR10 – Admin & QA**: View crawl status, error rates, sample parses, manual override of selectors, re‑crawl triggers.
- **FR11 – Internationalization**: Language detection; per‑locale tokenization and stemming; transliteration for search.
- **FR12 – Compliance**: Respect robots.txt, TOS; store fetch logs; honor takedown requests.

## 7. Non‑Functional Requirements
- **Freshness**: P95 ingestion latency < 30 minutes from publication; P99 < 90 minutes.
- **Reliability**: Ingestion pipeline SLO 99.5% over 30 days.
- **Scalability**: 1k–5k new items/day MVP; 50k/day v1; horizontal scale.
- **Accuracy**: Field extraction precision/recall ≥ 0.95 for core fields on MVP sources.
- **Search**: P95 query latency < 300 ms for typical filters; cold start < 1 s.
- **Cost**: Infra <$1,500/month MVP (ex‑labor) at target volume.
- **Security**: Secrets management, network egress control, PII‑free by design.

## 8. Data Sources (Initial List)
- **Magazines**: Vogue, Harper’s Bazaar, ELLE, GQ Style, W Magazine, Business of Fashion (public pages), Dazed, Hypebeast.
- **Brands**: Gucci, Louis Vuitton, Prada, Dior, Chanel, Balenciaga, Zara press.
- **Retailers/Blogs**: Ssense, Farfetch editorial, Net‑a‑Porter, Highsnobiety, TheFashionSpot.
- **Wires**: FashionUnited, Reuters Lifestyle (public), AP Lifestyle (public snippets).
- Prioritize sources with RSS/sitemaps; maintain source registry with compliance notes.

## 9. API Specification (MVP)
- **Auth**: API key header `X-API-Key` (project‑level). Rate limit: 60 req/min/key.
- **Endpoints**:
  - GET `/api/v1/articles`
    - Query: `q`, `brands[]`, `designers[]`, `categories[]`, `sources[]`, `lang`, `from`, `to`, `sort=publishedAt|relevance`, `page`, `pageSize`
    - Response: `{ items: Article[], total, facets: { brands, categories, sources, languages, dates } }`
  - GET `/api/v1/articles/{id}`
    - Response: `Article` with full text, media, entities, summary, canonical.
  - GET `/api/v1/trends`
    - Query: `window=24h|7d|30d`, `dimension=brands|topics|sources`, optional `lang`
    - Response: ranked items with counts and sparkline.
  - GET `/api/v1/sources`
    - List configured sources and health.

- **Article (schema)**:
  - `id`, `title`, `slug`, `canonicalUrl`, `sourceId`, `sourceName`, `authors[]`, `publishedAt`, `fetchedAt`, `language`, `categories[]`, `brands[]`, `designers[]`, `entities[]`, `summary`, `keywords[]`, `bodyHtml`, `bodyText`, `leadImageUrl`, `imageAttribution`, `wordCount`.

## 10. Data Model (Logical)
- **Tables/Indexes**:
  - `sources` (id, name, type, homepageUrl, rssUrl, sitemapUrl, robotsTxtUrl, crawlStrategy, active, crawlIntervalMinutes, lastSuccessAt, lastError, country, languageDefault)
  - `articles` (id, sourceId, canonicalUrl, urlHash, title, authors, publishedAt, fetchedAt, language, bodyHtml, bodyText, leadImageUrl, imageAttribution, wordCount, summary, createdAt, updatedAt)
  - `article_entities` (articleId, entityType, value, confidence, spanStart, spanEnd)
  - `article_categories` (articleId, category, confidence)
  - `article_media` (id, articleId, mediaType, url, caption, width, height, rights)
  - Search index: Elasticsearch/OpenSearch document mirrors `Article` with facets and analyzers.
- **Storage**:
  - Raw HTML, screenshots to object storage (e.g., S3 `raw/{sourceId}/{articleId}.html`).

## 11. Architecture (MVP)
- **Ingestion**: Scheduler → Queue → Fetcher workers (HTTP/Playwright for JS) → Parser (Readability + per‑source selectors) → Normalizer → Deduper → Enrichment (spaCy/transformer, rules) → Indexer.
- **Tech**:
  - Python (Scrapy + Playwright) for crawling; FastAPI for APIs; PostgreSQL for metadata; OpenSearch for search; Redis for queues/cache; S3‑compatible for blobs.
- **Ops**: Docker/K8s; Prometheus + Grafana; Loki/ELK for logs; Sentry for errors.
- **Compliance**: robots.txt parser; per‑domain rate limits; user‑agent and contact.

## 12. Monitoring & Alerting
- **Dashboards**: Ingestion throughput, latency, error rate per source, dedup rate, extraction accuracy samples, queue depth, API p95 latency.
- **Alerts**: Source failure >30 min, global error spike, index lag >60 min, API 5xx >1%.
- **QA**: Golden set of 100 articles/week with manual labeling to track extraction and classifier accuracy.

## 13. Security & Legal
- Secrets in vault; rotated keys.
- IP allowlist for admin; audit logs for admin actions.
- TOS/robots compliance; DMCA/takedown workflow; content rights metadata stored.

## 14. KPIs & Success Metrics
- Coverage: % of priority sources active (target ≥ 95%).
- Freshness: P95 latency from publish to index (target ≤ 30 min).
- Quality: Extraction F1 (target ≥ 0.95 for title/date/body on MVP sources).
- Enrichment: Brand/designer NER F1 (target ≥ 0.85 at MVP, ≥ 0.92 at v1).
- Dedup effectiveness: duplicate cluster rate ≤ 3%.
- API: p95 latency ≤ 300 ms; error rate ≤ 0.5%.

## 15. Release Plan & Milestones
- **M0 (2 wks)**: Tech spike, pick stack, build 5 sources end‑to‑end, baseline dashboards.
- **M1 (4 wks)**: MVP with 30 sources; EN only; REST API; admin basics; deploy.
- **M2 (4 wks)**: 75 sources; enrichment v1 (NER, categories, summary); trend endpoint; QA harness.
- **M3 (6 wks)**: 150 sources; multi‑language (FR/IT/ZH); runway/show schema; improved dedup.
- **M4 (ongoing)**: Source expansions, export jobs, newsletter module, cost/perf tuning.

## 16. Acceptance Criteria (MVP)
- ≥30 configured sources live and green for 7 consecutive days.
- P95 freshness ≤ 30 min on MVP sources.
- ≥95% extraction accuracy on core fields across weekly golden set.
- API endpoints deployed, authenticated, documented, with ≥99.5% 7‑day uptime.
- Admin shows per‑source health, last run status, sample parse view, re‑crawl action.

## 17. Risks & Mitigations
- **Robots/TOS restrictions**: Prefer RSS/sitemaps; drop non‑compliant; seek permissions.
- **JS‑heavy sites**: Use Playwright selectively; cache; backoff to RSS when possible.
- **Classifier drift**: Continuous labeling and retraining; monitor precision/recall.
- **Cost spikes**: Rate limits, headless pool tuning, dedupe early, archive raw HTML selectively.
- **Multi‑language accuracy**: Use locale models; phased rollout with quality gates.

## 18. Open Questions
- Do we need a lightweight public UI now or API‑only for MVP?
- Which regions/languages are highest priority after EN?
- Are there enterprise requirements (SSO, VPC peering) for early adopters?
- Data export formats needed (CSV, Parquet to S3, BigQuery sync)?

## 19. Appendix: Initial Source Candidates (MVP)
- Vogue (EN), Harper’s Bazaar, ELLE, GQ Style, W Magazine, Business of Fashion (public), Dazed, Hypebeast, Highsnobiety, TheFashionSpot
- Brand pressrooms: Gucci, Louis Vuitton, Prada, Dior, Chanel, Balenciaga, Zara
- Retailers/blogs: Ssense, Farfetch editorial, Net‑a‑Porter
- Wires: FashionUnited, Reuters Lifestyle (public pages)