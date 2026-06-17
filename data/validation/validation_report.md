# EventLens Validation Report

Generated: `2026-06-17T13:07:02Z`

- Brier rows: 625
- Eligible Brier rows: 625
- Unique resolved markets: 566
- Primary analysis rows: 21
- Markets excluded from primary (no 24h-prior snapshot): 545
- Mean Brier: 0.1451
- Trust vs Brier correlation: -0.5081 (n=21)
- Trust vs Brier excluding missing spreads: -0.4652 (n=14)
- Trust vs Brier high-data-quality only: -0.5489 (n=10)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1740 | 3 |
| 40-55 | 0.1979 | 9 |
| 55-70 | 0.1012 | 7 |
| 70-85 | 0.0182 | 2 |
| 85-100 | N/A | 0 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1386 | 16 |
| 8-30d | 0.2040 | 3 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Formula 1 | 0.2293 | 4 |
| Sports | 0.1766 | 4 |
| Weather | 0.0001 | 4 |
| UFC | 0.1445 | 2 |
| 2026 FIFA World Cup | 0.1564 | 1 |
| Head coach | 0.1806 | 1 |
| Middle East | 0.2070 | 1 |
| Politics | 0.0001 | 1 |
| Soccer | 0.2704 | 1 |
| Solana | 0.1122 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1393 | 16 |
| sports_outcome | 0.2234 | 3 |
| Unknown | 0.0363 | 1 |
| crypto_price | 0.1122 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1437 | 10 |
| low | 0.1506 | 6 |
| Unknown | 0.1413 | 5 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.1952 | 13 |
| short_horizon | 0.0443 | 6 |
| Unknown | 0.0363 | 1 |
| category_diverse | 0.2070 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 545
- Mean Brier: 0.0824
- Trust vs Brier correlation: -0.2476 (n=545)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0363 | N/A | 1 |
| v0.2 | 0.0847 | -0.2590 | 566 |
