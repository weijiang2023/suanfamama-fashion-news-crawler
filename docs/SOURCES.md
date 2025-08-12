# Sources Guide · RunwayBase Agent

This document explains how to add, configure, and maintain content sources.

## Source types
- RSS: Preferred, reliable delta discovery.
- Sitemap: Good for discovery; combine with HTML parsing.
- HTML: Crawl listing pages and article pages with selectors.
- JS-rendered: Use Playwright; last resort due to cost.

## Source registry fields
- `id` (string): unique, e.g., `src_vogue`
- `name` (string): human-readable
- `type` (enum): `magazine|brand|retailer|wire|blog`
- `homepageUrl`, `rssUrl?`, `sitemapUrl?`, `robotsTxtUrl?`
- `crawlStrategy` (enum): `rss|sitemap|html|js`
- `crawlIntervalMinutes` (int): polling interval
- `languageDefault` (ISO 639-1): e.g., `en`
- `selectors` (object): per-source CSS/XPath for article pages
- `complianceNotes` (string): robots/TOS notes

## Selectors (article page)
Provide best-effort selectors, with fallbacks.
```
{
  "title": "h1.headline, h1.article-title",
  "author": ".byline a, .byline",
  "date": "time[datetime], .pub-date",
  "body": "article .content, .article-body",
  "leadImage": "meta[property='og:image']",
  "tags": ".tags a"
}
```
- Prefer semantic tags; avoid brittle nth-child.
- For dates, prefer machine-readable attributes (datetime) and parse timezone.

## HTML cleaning rules
- Remove scripts, styles, ads, share widgets, unrelated galleries.
- Convert relative URLs to absolute using page URL.
- Preserve basic formatting (p, h1–h3, em, strong, ul/ol, img captions).

## Discovery strategy
- RSS: poll at `crawlIntervalMinutes` (min 5m), dedupe by GUID/link.
- Sitemap: diff new `loc` values; prioritize recent `lastmod`.
- HTML listings: paginate up to a freshness window (e.g., 48h) and stop.

## Politeness & limits
- Respect robots.txt; skip disallowed paths.
- Per-host concurrency caps (e.g., 2) and delay (e.g., 1–2s).
- Backoff on 4xx/5xx; circuit-breaker after repeated failures.

## JS-rendered guidance
- Only for essential sources; block images/media to reduce cost.
- Wait for `networkidle` + key selector presence.
- Timeout per page (e.g., 15s) with 1–2 retries max.

## Adding a new source (checklist)
- [ ] Verify robots.txt and TOS allow crawling
- [ ] Identify discovery path (RSS, sitemap, listing)
- [ ] Implement/selectors and test on 5–10 sample URLs
- [ ] Define `crawlIntervalMinutes` based on publish cadence
- [ ] Add to registry with compliance notes
- [ ] Run a dry-run and validate extraction accuracy (≥95% core fields)
- [ ] Add to monitoring dashboard with error budget

## Maintenance
- Track selector drift via 4xx/parse-fail metrics
- Keep a small golden set of article URLs for regression tests
- Review error logs weekly; update selectors or switch to RSS/Sitemap