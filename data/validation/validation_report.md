# EventLens Validation Report

Generated: `2026-06-16T18:56:56Z`

- Brier rows: 505
- Eligible Brier rows: 505
- Unique resolved markets: 446
- Primary analysis rows: 19
- Markets excluded from primary (no 24h-prior snapshot): 427
- Mean Brier: 0.1426
- Trust vs Brier correlation: -0.5322 (n=19)
- Trust vs Brier excluding missing spreads: -0.4901 (n=12)
- Trust vs Brier high-data-quality only: -0.5653 (n=8)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1849 | 1 |
| 40-55 | 0.1979 | 9 |
| 55-70 | 0.1012 | 7 |
| 70-85 | 0.0182 | 2 |
| 85-100 | N/A | 0 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1375 | 15 |
| 8-30d | 0.2040 | 3 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Formula 1 | 0.2293 | 4 |
| Sports | 0.1766 | 4 |
| Weather | 0.0001 | 4 |
| UFC | 0.1445 | 2 |
| Middle East | 0.2070 | 1 |
| Politics | 0.0001 | 1 |
| Soccer | 0.2704 | 1 |
| Solana | 0.1122 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1351 | 14 |
| sports_outcome | 0.2234 | 3 |
| Unknown | 0.0363 | 1 |
| crypto_price | 0.1122 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1375 | 8 |
| low | 0.1506 | 6 |
| Unknown | 0.1413 | 5 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2001 | 11 |
| short_horizon | 0.0443 | 6 |
| Unknown | 0.0363 | 1 |
| category_diverse | 0.2070 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 427
- Mean Brier: 0.0710
- Trust vs Brier correlation: -0.3248 (n=427)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0363 | N/A | 1 |
| v0.2 | 0.0741 | -0.3346 | 446 |
