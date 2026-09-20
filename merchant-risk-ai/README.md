# Merchant Risk AI

An AI-powered, defense-only risk management system for detecting high-risk e-commerce orders and helping merchants reduce financial loss.

## Current focus

Return/fraud risk scoring.

## Planned pipeline

Data → Features → ML Risk Model → Risk Score → Explainability → Business Action

## Current dataset

Stage 2 provides a reproducible, synthetic e-commerce transaction dataset for development. See [data/DATASET.md](data/DATASET.md) for its schema, limitations, and generation command.

## Current exploration

Stage 3 adds schema validation and deterministic, per-order exploratory features. See [docs/feature_engineering.md](docs/feature_engineering.md). No model has been trained and no held-out test evaluation exists.

No model or scoring logic has been implemented.
