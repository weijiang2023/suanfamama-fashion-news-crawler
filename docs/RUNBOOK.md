# Operations Runbook · RunwayBase Agent

Step-by-step procedures for common incidents and maintenance.

## 1) Source parsing failures
- Symptom: `parse_failure_total{source}` rising
- Action:
  1. Open logs filtered by `sourceId`
  2. Inspect sample HTML; verify selectors
  3. Hotfix selectors via admin override
  4. Re-run backfill for last 24–48h

## 2) Crawl bans / 403s
- Symptom: sustained 403s; robots updates
- Action:
  1. Halt jobs for the source (circuit breaker)
  2. Verify robots.txt/TOS; adjust paths or drop source
  3. Reduce rate limits and concurrency
  4. If permissible, rotate exit IP within policy

## 3) JS fetcher instability
- Symptom: timeouts, OOMs, high error rate
- Action:
  1. Reduce JS worker concurrency
  2. Enable resource blocking (images, fonts)
  3. Increase timeout slightly; add wait-for selector
  4. Prefer RSS/Sitemap if available

## 4) Index lag
- Symptom: high ingestion latency, stale search
- Action:
  1. Check queue depth and worker metrics
  2. Scale indexer and workers
  3. Investigate slow mapping or heavy analyzers
  4. Bulk reindex if needed (off-peak)

## 5) Bad enrichment (drift)
- Symptom: lower NER/classifier accuracy
- Action:
  1. Review golden set metrics
  2. Retrain on latest labels; A/B deploy
  3. Roll back on regression

## 6) Data corruption / duplicates
- Symptom: sudden duplicate clusters or missing fields
- Action:
  1. Validate dedup logic and hashes
  2. Run integrity checks; restore from backups if needed
  3. Reprocess affected window

## 7) Secrets leaked/rotated
- Action:
  1. Revoke leaked credentials
  2. Rotate secrets in vault and redeploy
  3. Audit logs for abuse

## Contacts & Escalation
- Add on-call rotations and Slack channels here