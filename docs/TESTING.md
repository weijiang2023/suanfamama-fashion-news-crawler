# Testing & QA · RunwayBase Agent

## Strategy
- Unit tests: parsing utilities, normalizer, enrichment components.
- Integration tests: end-to-end ingestion for sample sources (mocked network).
- Golden set QA: weekly 100-article labeled sample to track extraction and classifier metrics.

## Tools
- Python test framework (pytest), coverage >80% on core logic.
- Snapshot tests for parser outputs and index documents.

## Golden set process
- Curate URLs across source types and languages.
- Label core fields and entities; store in versioned dataset.
- Run evaluation in CI; fail builds on metric regression beyond thresholds.

## CI/CD
- Lint, type-check, unit tests on PRs.
- Integration tests and golden set metrics on main nightly.