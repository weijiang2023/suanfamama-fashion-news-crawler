# Deployment · RunwayBase Agent

## Environments
- Staging: feature validation, lower quotas.
- Production: full quotas, SLO-backed.

## Infrastructure
- Kubernetes (recommended) with managed PostgreSQL, OpenSearch, Redis, and S3-compatible storage.
- Separate node pools for JS workers vs. API.

## Secrets & config
- Mounted from vault; environment variables documented in `ENV_VARS.md`.
- ConfigMaps for static config (taxonomy snapshots, source registry defaults).

## Deploy steps (outline)
1. Build images: `api`, `workers-http`, `workers-js`, `indexer`, `scheduler`.
2. Apply migrations (Alembic).
3. Apply OpenSearch index templates/mappings.
4. Deploy manifests/Helm charts.
5. Scale workers based on queue depth.
6. Warm caches with recent sources.

## Rollbacks
- Use deployment revisions; roll back images.
- For index changes, write to new index alias and swap on success.

## Observability
- Enable dashboards and alerts per `OBSERVABILITY.md`.