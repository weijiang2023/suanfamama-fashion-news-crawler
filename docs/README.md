# Documentation · RunwayBase Agent

An agent on a vertical fashion knowledgebase that discovers, enriches, and answers—purpose‑built for runway and brand intelligence.

## Quick links
- PRD: `docs/PRD.md`
- Architecture: `docs/ARCHITECTURE.md`
- API Reference: `docs/API.md`
- Setup: `docs/SETUP.md`

## Who this is for
- Product, engineering, and data teams working on RunwayBase Agent
- External stakeholders reviewing requirements and APIs

## Onboarding (high-level)
Until full setup scripts are added, use this as a guide.

1) Read the docs
- Start with the PRD to understand scope and KPIs
- Review the Architecture for components and data flow
- Review the API for endpoints and schemas

2) Local development (placeholder)
- Prerequisites: Docker, Python 3.11+, Node 18+ (if admin UI is included)
- Create a `.env` with required secrets (to be defined in setup guide)
- Recommended stack (per PRD): FastAPI, PostgreSQL, OpenSearch, Redis, S3-compatible storage, Playwright workers
- A `docker-compose` dev environment will be added here when services are implemented

3) Contribution workflow
- Branch naming: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`
- Commits: Conventional Commits (e.g., `feat(ingestion): add sitemap discovery`)
- PRs: small, focused, with screenshots/log samples when relevant
- Testing: include unit tests for extraction/parsing rules and enrichment

## Glossary (short)
- Brand/Designer: Named fashion entities used for tagging and filters
- Runway/Show: Event metadata (brand, season, city, collection)
- Category: One of {Runway, Trend, Retail, Celebrity, Business, Sustainability, Beauty, Street Style}
- Enrichment: NER, classification, summarization, and schema detection

## Contact
- User‑agent string should identify as RunwayBase Agent and include a contact URL/email
- For internal questions: add maintainers and Slack channel here