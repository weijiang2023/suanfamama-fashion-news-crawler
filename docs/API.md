# API Reference: RunwayBase Agent

Version: v1 (MVP)
Base URL: https://api.runwaybase.example.com
Auth: API key via header `X-API-Key`
Rate limit: 60 requests/minute per key (429 on limit)

## Conventions
- Dates: ISO 8601 (e.g., `2025-08-12T14:30:00Z`)
- Pagination: `page` (1-based), `pageSize` (default 20, max 100)
- Arrays in query: repeat params (e.g., `brands=Gucci&brands=Dior`)
- Errors: JSON `{ error: { code, message, details? } }`

## Authentication
Send header: `X-API-Key: <your-key>`

Errors:
- 401 Unauthorized: missing/invalid key
- 429 Too Many Requests: rate limit exceeded

## Resources

### Articles

GET /api/v1/articles
- Description: Search and list articles with filters and facets.
- Query params:
  - `q` (string): full text query
  - `brands` (repeatable): brand filter
  - `designers` (repeatable): designer filter
  - `categories` (repeatable): category filter
  - `sources` (repeatable): source filter (source IDs or names)
  - `lang` (string): ISO 639-1 language code
  - `from` (datetime): publishedAt lower bound
  - `to` (datetime): publishedAt upper bound
  - `sort` (string): `publishedAt` (default) or `relevance`
  - `page` (int): default 1
  - `pageSize` (int): default 20, max 100
- Response 200:
```
{
  "items": [
    {
      "id": "a_01HXT...",
      "title": "Gucci unveils FW24 collection in Milan",
      "canonicalUrl": "https://...",
      "sourceId": "src_vogue",
      "sourceName": "Vogue",
      "authors": ["Jane Doe"],
      "publishedAt": "2025-08-12T09:00:00Z",
      "fetchedAt": "2025-08-12T09:05:12Z",
      "language": "en",
      "categories": ["Runway"],
      "brands": ["Gucci"],
      "designers": ["Sabato De Sarno"],
      "entities": [{"type": "location", "value": "Milan", "confidence": 0.91}],
      "summary": "Three-sentence recap of highlights...",
      "keywords": ["FW24", "Milan Fashion Week"],
      "leadImageUrl": "https://.../lead.jpg",
      "imageAttribution": "Vogue",
      "wordCount": 854
    }
  ],
  "total": 1234,
  "facets": {
    "brands": [{"value": "Gucci", "count": 87}],
    "categories": [{"value": "Runway", "count": 203}],
    "sources": [{"value": "Vogue", "count": 112}],
    "languages": [{"value": "en", "count": 1000}],
    "dates": [{"value": "2025-08-12", "count": 54}]
  }
}
```
- Errors: 400 (invalid params)

GET /api/v1/articles/{id}
- Path params: `id` (string)
- Response 200:
```
{
  "id": "a_01HXT...",
  "title": "Gucci unveils FW24 collection in Milan",
  "slug": "gucci-fw24-milan",
  "canonicalUrl": "https://...",
  "sourceId": "src_vogue",
  "sourceName": "Vogue",
  "authors": ["Jane Doe"],
  "publishedAt": "2025-08-12T09:00:00Z",
  "fetchedAt": "2025-08-12T09:05:12Z",
  "language": "en",
  "categories": ["Runway"],
  "brands": ["Gucci"],
  "designers": ["Sabato De Sarno"],
  "entities": [{"type": "location", "value": "Milan", "confidence": 0.91}],
  "summary": "Three-sentence recap of highlights...",
  "keywords": ["FW24", "Milan Fashion Week"],
  "bodyHtml": "<p>...</p>",
  "bodyText": "...",
  "leadImageUrl": "https://.../lead.jpg",
  "imageAttribution": "Vogue",
  "wordCount": 854
}
```
- Errors: 404 (not found)

### Trends

GET /api/v1/trends
- Description: Returns trending items over a time window.
- Query params:
  - `window`: `24h` | `7d` | `30d`
  - `dimension`: `brands` | `topics` | `sources`
  - `lang` (optional)
- Response 200:
```
{
  "dimension": "brands",
  "window": "24h",
  "items": [
    {"value": "Gucci", "count": 87, "spark": [2,3,4,6,8,9]},
    {"value": "Dior", "count": 65, "spark": [1,2,2,3,4,7]}
  ]
}
```

### Sources

GET /api/v1/sources
- Description: Lists configured sources and health snapshot.
- Response 200:
```
[
  {
    "id": "src_vogue",
    "name": "Vogue",
    "type": "magazine",
    "homepageUrl": "https://www.vogue.com",
    "rssUrl": "https://www.vogue.com/rss",
    "sitemapUrl": "https://www.vogue.com/sitemap.xml",
    "crawlStrategy": "rss|sitemap|html|js",
    "active": true,
    "crawlIntervalMinutes": 15,
    "lastSuccessAt": "2025-08-12T09:10:00Z",
    "lastError": null,
    "languageDefault": "en"
  }
]
```

## Schemas

Article
```
{
  "id": "string",
  "title": "string",
  "slug": "string",
  "canonicalUrl": "string",
  "sourceId": "string",
  "sourceName": "string",
  "authors": ["string"],
  "publishedAt": "datetime",
  "fetchedAt": "datetime",
  "language": "string",
  "categories": ["string"],
  "brands": ["string"],
  "designers": ["string"],
  "entities": [Entity],
  "summary": "string",
  "keywords": ["string"],
  "bodyHtml": "string",
  "bodyText": "string",
  "leadImageUrl": "string",
  "imageAttribution": "string",
  "wordCount": 0
}
```

Entity
```
{ "type": "brand|designer|location|event|person", "value": "string", "confidence": 0.0 }
```

FacetItem
```
{ "value": "string", "count": 0 }
```

Error
```
{ "error": { "code": "string", "message": "string", "details": {} } }
```

## Status Codes
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error

## Changelog
- v1 (MVP): articles, article detail, trends, sources