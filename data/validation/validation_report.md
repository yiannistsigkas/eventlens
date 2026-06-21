# EventLens Validation Report

Generated: `2026-06-21T10:13:39Z`

- Brier rows: 1075
- Eligible Brier rows: 1075
- Unique resolved markets: 950
- Primary analysis rows: 82
- Markets excluded from primary (no 24h-prior snapshot): 868
- Mean Brier: 0.1526
- Trust vs Brier correlation: -0.3606 (n=82)
- Trust vs Brier excluding missing spreads: -0.2604 (n=55)
- Trust vs Brier high-data-quality only: -0.2530 (n=49)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1899 | 11 |
| 40-55 | 0.2080 | 41 |
| 55-70 | 0.0773 | 24 |
| 70-85 | 0.0073 | 5 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1722 | 64 |
| 8-30d | 0.1061 | 9 |
| 31-90d | 0.0457 | 7 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2196 | 33 |
| Weather | 0.0001 | 10 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2426 | 4 |
| Formula 1 | 0.2293 | 4 |
| Recurring | 0.0789 | 4 |
| ice hockey | 0.0001 | 4 |
| 2026 FIFA World Cup | 0.0535 | 3 |
| Politics | 0.2746 | 3 |
| Solana | 0.1443 | 2 |
| UFC | 0.1445 | 2 |
| XRP | 0.1558 | 2 |
| FIFA World Cup | 0.0005 | 1 |
| Head coach | 0.1806 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| Soccer | 0.2704 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1060 | 41 |
| sports_prop | 0.2634 | 21 |
| sports_outcome | 0.1526 | 11 |
| crypto_price | 0.1145 | 8 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1585 | 49 |
| low | 0.1510 | 25 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2170 | 50 |
| short_horizon | 0.0219 | 13 |
| medium_horizon | 0.0360 | 9 |
| category_diverse | 0.0345 | 6 |
| top_volume | 0.2685 | 3 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 868
- Mean Brier: 0.0774
- Trust vs Brier correlation: -0.2355 (n=868)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0182 | N/A | 2 |
| v0.2 | 0.0833 | -0.2759 | 950 |
