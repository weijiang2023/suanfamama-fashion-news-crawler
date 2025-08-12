# Environment Variables · RunwayBase Agent

| Name | Example | Description |
|---|---|---|
| POSTGRES_USER | runwaybase | Postgres user |
| POSTGRES_PASSWORD | runwaybase | Postgres password |
| POSTGRES_DB | runwaybase | Postgres database name |
| DATABASE_URL | postgresql://runwaybase:runwaybase@localhost:5432/runwaybase | SQLAlchemy connection string |
| OPENSEARCH_HOST | http://localhost:9200 | OpenSearch endpoint |
| REDIS_URL | redis://localhost:6379/0 | Redis connection URL |
| MINIO_ROOT_USER | runwaybase | MinIO root user (local) |
| MINIO_ROOT_PASSWORD | runwaybase123 | MinIO root password (local) |
| S3_ENDPOINT | http://localhost:9000 | S3-compatible endpoint |
| S3_ACCESS_KEY_ID | runwaybase | Access key for S3/MinIO |
| S3_SECRET_ACCESS_KEY | runwaybase123 | Secret key for S3/MinIO |
| S3_BUCKET | runwaybase-raw | Bucket for raw HTML/screenshots |
| API_PORT | 8080 | API listen port |
| X_API_KEY | (set in prod) | API key for client auth |