# EventLens Validation Report

Generated: `2026-06-24T10:15:09Z`

- Brier rows: 1343
- Eligible Brier rows: 1343
- Unique resolved markets: 1213
- Primary analysis rows: 114
- Markets excluded from primary (no 24h-prior snapshot): 1099
- Mean Brier: 0.1499
- Trust vs Brier correlation: -0.3888 (n=114)
- Trust vs Brier excluding missing spreads: -0.2522 (n=72)
- Trust vs Brier high-data-quality only: -0.2476 (n=66)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2042 | 29 |
| 40-55 | 0.1908 | 46 |
| 55-70 | 0.0734 | 32 |
| 70-85 | 0.0061 | 6 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1675 | 93 |
| 8-30d | 0.0808 | 12 |
| 31-90d | 0.0457 | 7 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2022 | 56 |
| Weather | 0.0309 | 16 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2426 | 4 |
| Formula 1 | 0.2293 | 4 |
| Recurring | 0.0789 | 4 |
| ice hockey | 0.0001 | 4 |
| 2026 FIFA World Cup | 0.0535 | 3 |
| Politics | 0.2746 | 3 |
| XRP | 0.1072 | 3 |
| Solana | 0.1443 | 2 |
| UFC | 0.1445 | 2 |
| FIFA World Cup | 0.0005 | 1 |
| Head coach | 0.1806 | 1 |
| Highest temperature | 0.0000 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| Soccer | 0.2704 | 1 |
| le mans | 0.2070 | 1 |
| transit | 0.0000 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.0988 | 49 |
| sports_prop | 0.2403 | 31 |
| sports_outcome | 0.1598 | 24 |
| crypto_price | 0.1029 | 9 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1360 | 66 |
| low | 0.1785 | 40 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2074 | 72 |
| short_horizon | 0.0389 | 20 |
| medium_horizon | 0.0296 | 11 |
| category_diverse | 0.0296 | 7 |
| top_volume | 0.2685 | 3 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1099
- Mean Brier: 0.0795
- Trust vs Brier correlation: -0.2439 (n=1099)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0182 | N/A | 2 |
| v0.2 | 0.0857 | -0.2898 | 1213 |
