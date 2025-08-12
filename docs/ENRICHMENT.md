# Enrichment · RunwayBase Agent

This document describes entity extraction, classification, summarization, and taxonomy.

## Taxonomy
- Entities: brand, designer, person, location, event (e.g., Fashion Week city)
- Categories: Runway, Trend, Retail, Celebrity, Business, Sustainability, Beauty, Street Style
- Gazetteers: curated lists of brands/designers with aliases and normalization rules

## Entity extraction (NER)
- Approach: hybrid gazetteer + ML (spaCy/transformer fine-tuned on fashion text)
- Output fields: `entityType`, `value`, `confidence`, optional spans
- Normalization: map aliases (e.g., "LV" → "Louis Vuitton")

## Category classification
- Multilabel classifier; confidence threshold (e.g., 0.5) with abstention
- Training data: labeled articles from MVP sources; maintain validation split
- Drift monitoring: track precision/recall monthly against a golden set

## Summarization
- 2–3 sentence abstractive summary focused on key facts (brand, collection, location, highlights)
- Safety: remove hallucinated facts; prefer extractive fallback on low confidence

## Keywords
- Combination of TextRank and N-gram frequency with entity boosts

## Runway/Show schema detection
- Heuristics + classifier to detect runway/show context
- Extract: brand, season (e.g., SS25, FW24), city (e.g., Paris), collection name if present

## Quality metrics
- NER F1 (by entity type), classification F1 (by category), summary ROUGE/L
- Acceptance gates defined in PRD (e.g., NER F1 ≥ 0.85 MVP)

## Evaluation & labeling
- Maintain weekly 100-article golden set; rotate sources
- Use a simple annotation tool or CSV schema for labels

## Versioning
- Tag enrichment model versions; store in metadata on each article
- Rollout with canary and rollback on metric regression