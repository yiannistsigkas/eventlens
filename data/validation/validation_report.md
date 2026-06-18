# EventLens Validation Report

Generated: `2026-06-18T11:17:46Z`

- Brier rows: 748
- Eligible Brier rows: 748
- Unique resolved markets: 652
- Primary analysis rows: 41
- Markets excluded from primary (no 24h-prior snapshot): 611
- Mean Brier: 0.1591
- Trust vs Brier correlation: -0.2630 (n=41)
- Trust vs Brier excluding missing spreads: -0.1892 (n=30)
- Trust vs Brier high-data-quality only: -0.1756 (n=25)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1778 | 4 |
| 40-55 | 0.2453 | 16 |
| 55-70 | 0.1157 | 16 |
| 70-85 | 0.0091 | 4 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1536 | 35 |
| 8-30d | 0.2040 | 3 |
| 31-90d | 0.3192 | 1 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2729 | 10 |
| Weather | 0.0001 | 8 |
| Economic Policy | 0.0000 | 5 |
| Formula 1 | 0.2293 | 4 |
| Politics | 0.2746 | 3 |
| UFC | 0.1445 | 2 |
| XRP | 0.1558 | 2 |
| 2026 FIFA World Cup | 0.1564 | 1 |
| Head coach | 0.1806 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| Soccer | 0.2704 | 1 |
| Solana | 0.1122 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1204 | 28 |
| sports_prop | 0.3666 | 5 |
| sports_outcome | 0.2149 | 4 |
| crypto_price | 0.1412 | 3 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1866 | 25 |
| low | 0.1134 | 10 |
| Unknown | 0.1208 | 6 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2320 | 21 |
| short_horizon | 0.0258 | 11 |
| category_diverse | 0.0345 | 6 |
| Unknown | 0.0363 | 1 |
| medium_horizon | 0.3192 | 1 |
| top_volume | 0.8055 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 611
- Mean Brier: 0.0847
- Trust vs Brier correlation: -0.2728 (n=611)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0363 | N/A | 1 |
| v0.2 | 0.0884 | -0.2790 | 652 |
