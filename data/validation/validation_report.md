# EventLens Validation Report

Generated: `2026-06-22T11:06:31Z`

- Brier rows: 1145
- Eligible Brier rows: 1145
- Unique resolved markets: 1020
- Primary analysis rows: 89
- Markets excluded from primary (no 24h-prior snapshot): 931
- Mean Brier: 0.1461
- Trust vs Brier correlation: -0.3892 (n=89)
- Trust vs Brier excluding missing spreads: -0.2851 (n=59)
- Trust vs Brier high-data-quality only: -0.2810 (n=53)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1799 | 13 |
| 40-55 | 0.2088 | 42 |
| 55-70 | 0.0688 | 27 |
| 70-85 | 0.0061 | 6 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1621 | 71 |
| 8-30d | 0.1061 | 9 |
| 31-90d | 0.0457 | 7 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2149 | 36 |
| Weather | 0.0002 | 13 |
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
| Highest temperature | 0.0000 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| Soccer | 0.2704 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.0966 | 45 |
| sports_prop | 0.2509 | 24 |
| sports_outcome | 0.1526 | 11 |
| crypto_price | 0.1145 | 8 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1467 | 53 |
| low | 0.1520 | 28 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2140 | 53 |
| short_horizon | 0.0168 | 17 |
| medium_horizon | 0.0360 | 9 |
| category_diverse | 0.0345 | 6 |
| top_volume | 0.2685 | 3 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 931
- Mean Brier: 0.0772
- Trust vs Brier correlation: -0.2436 (n=931)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0182 | N/A | 2 |
| v0.2 | 0.0827 | -0.2846 | 1020 |
