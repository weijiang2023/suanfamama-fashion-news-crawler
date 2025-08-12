# Local Setup · RunwayBase Agent

This guide brings up local infrastructure (databases, search, cache, object storage) for development.

## Prerequisites
- Docker Desktop or Docker Engine + Compose
- `curl`, `jq` (optional)

## 1) Clone and prepare env
```bash
cp .env.example .env
```
Edit `.env` if needed (passwords, ports, bucket names).

## 2) Start infra
```bash
docker compose up -d
```
This starts:
- PostgreSQL (5432)
- OpenSearch (9200) and Dashboards (5601)
- Redis (6379)
- MinIO (9000 API, 9001 Console)

## 3) Verify services
- OpenSearch:
```bash
curl -s http://localhost:9200 | jq .
```
- Postgres:
```bash
PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "select now();"
```
- Redis:
```bash
redis-cli -h localhost ping
```
- MinIO Console: visit http://localhost:9001 and log in with `${MINIO_ROOT_USER}` / `${MINIO_ROOT_PASSWORD}`

## 4) Create S3 bucket (MinIO)
Use MinIO console (UI) or CLI:
```bash
docker run --rm --network host \
  -e MC_HOST_local=http://${MINIO_ROOT_USER}:${MINIO_ROOT_PASSWORD}@localhost:9000 \
  minio/mc:latest \
  sh -c "mc alias set local http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} && mc mb -p local/${S3_BUCKET} || true && mc anonymous set download local/${S3_BUCKET}"
```

## 5) Notes
- OpenSearch security is disabled for local dev. Do not expose ports publicly.
- Data is persisted in Docker volumes: `pgdata`, `osdata`, `minio`.
- To reset data: `docker compose down -v` (this deletes volumes).

## 6) Next steps
- Implement API and workers using the stack in `docs/ARCHITECTURE.md`.
- Add migrations for PostgreSQL (Alembic or similar).
- Add index templates/mappings for OpenSearch.
- Wire `.env` variables in services.