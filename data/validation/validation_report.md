# EventLens Validation Report

Generated: `2026-06-14T16:00:42Z`

- Brier rows: 322
- Eligible Brier rows: 322
- Unique resolved markets: 273
- Primary analysis rows: 3
- Markets excluded from primary (no 24h-prior snapshot): 270
- Mean Brier: 0.0782
- Trust vs Brier correlation: -0.7583 (n=3)
- Trust vs Brier excluding missing spreads: -1.0000 (n=2)
- Trust vs Brier high-data-quality only: N/A (n=0)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | N/A | 0 |
| 40-55 | 0.1980 | 1 |
| 55-70 | 0.0001 | 1 |
| 70-85 | 0.0363 | 1 |
| 85-100 | N/A | 0 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.0001 | 1 |
| 8-30d | 0.1980 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1172 | 2 |
| Politics | 0.0001 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| Unknown | 0.0363 | 1 |
| news_event | 0.0001 | 1 |
| sports_outcome | 0.1980 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| Unknown | 0.0782 | 3 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| Unknown | 0.0363 | 1 |
| low_liquidity | 0.1980 | 1 |
| short_horizon | 0.0001 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 270
- Mean Brier: 0.0911
- Trust vs Brier correlation: -0.2500 (n=270)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0363 | N/A | 1 |
| v0.2 | 0.0909 | -0.2551 | 273 |
