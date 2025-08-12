# Observability · RunwayBase Agent

This document outlines metrics, logs, dashboards, and alerting standards.

## Metrics (Prometheus)
- Ingestion
  - `jobs_enqueued_total{source}`
  - `fetch_duration_seconds_bucket{source}` (histogram)
  - `fetch_failures_total{source,code}`
  - `parse_success_total{source}` / `parse_failure_total{source}`
  - `ingestion_latency_seconds` (publish→index)
  - `dedup_ratio`
- Enrichment
  - `ner_runtime_seconds_bucket`
  - `classification_confidence_bucket{category}`
- API
  - `http_server_requests_seconds_bucket{route,status}`
  - `search_hits_total{route}`
  - `search_latency_ms_bucket`
- Workers/Queue
  - `queue_depth`
  - `worker_active{type}`

## Logs
- Structured JSON logs: `timestamp`, `level`, `component`, `sourceId`, `articleId`, `message`, `traceId`
- Correlate fetch→parse→index via `traceId`

## Dashboards (Grafana)
- Ingestion Health: throughput, failures by source, latency p95
- Enrichment Quality: NER/classifier confidence distributions, sample errors
- API Performance: latency percentiles, error rates, QPS
- Queue/Workers: depth over time, concurrency, retries

## Alerts
- Source failure >30m (no success)
- Global error spike (5xx or parse failures > threshold)
- Index lag >60m
- API 5xx >1% over 5m
- Playwright failure surge or timeouts

## SLOs
- Ingestion availability 99.5%
- API p95 latency <300 ms
- Freshness P95 <30 min