# EventLens Validation Report

Generated: `2026-06-25T07:05:06Z`

- Brier rows: 1495
- Eligible Brier rows: 1495
- Unique resolved markets: 1332
- Primary analysis rows: 136
- Markets excluded from primary (no 24h-prior snapshot): 1196
- Mean Brier: 0.1478
- Trust vs Brier correlation: -0.4223 (n=136)
- Trust vs Brier excluding missing spreads: -0.2849 (n=83)
- Trust vs Brier high-data-quality only: -0.2823 (n=77)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2034 | 35 |
| 40-55 | 0.1856 | 57 |
| 55-70 | 0.0653 | 36 |
| 70-85 | 0.0078 | 7 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1720 | 104 |
| 8-30d | 0.0702 | 21 |
| 31-90d | 0.0591 | 9 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1887 | 76 |
| Weather | 0.0309 | 16 |
| Economic Policy | 0.0000 | 5 |
| 2026 FIFA World Cup | 0.0402 | 4 |
| Finance | 0.2426 | 4 |
| Formula 1 | 0.2293 | 4 |
| Recurring | 0.0789 | 4 |
| ice hockey | 0.0001 | 4 |
| Politics | 0.2746 | 3 |
| XRP | 0.1072 | 3 |
| FIFA World Cup | 0.0003 | 2 |
| Solana | 0.1443 | 2 |
| UFC | 0.1445 | 2 |
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
| news_event | 0.0949 | 51 |
| sports_prop | 0.2321 | 45 |
| sports_outcome | 0.1286 | 30 |
| crypto_price | 0.1029 | 9 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1288 | 77 |
| low | 0.1808 | 51 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2085 | 86 |
| short_horizon | 0.0389 | 20 |
| medium_horizon | 0.0205 | 17 |
| category_diverse | 0.0296 | 7 |
| top_volume | 0.1611 | 5 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1196
- Mean Brier: 0.0800
- Trust vs Brier correlation: -0.2766 (n=1196)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0091 | 0.5613 | 4 |
| v0.2 | 0.0865 | -0.3230 | 1332 |
