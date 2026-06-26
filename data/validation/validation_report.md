# EventLens Validation Report

Generated: `2026-06-26T16:08:09Z`

- Brier rows: 1704
- Eligible Brier rows: 1704
- Unique resolved markets: 1516
- Primary analysis rows: 168
- Markets excluded from primary (no 24h-prior snapshot): 1348
- Mean Brier: 0.1522
- Trust vs Brier correlation: -0.4761 (n=168)
- Trust vs Brier excluding missing spreads: -0.3216 (n=93)
- Trust vs Brier high-data-quality only: -0.3207 (n=87)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2098 | 42 |
| 40-55 | 0.1934 | 73 |
| 55-70 | 0.0589 | 44 |
| 70-85 | 0.0068 | 8 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1717 | 129 |
| 8-30d | 0.0955 | 28 |
| 31-90d | 0.0591 | 9 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1976 | 99 |
| Weather | 0.0307 | 24 |
| 2026 FIFA World Cup | 0.0321 | 5 |
| Economic Policy | 0.0000 | 5 |
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
| news_event | 0.0847 | 60 |
| sports_prop | 0.2334 | 60 |
| sports_outcome | 0.1454 | 38 |
| crypto_price | 0.1029 | 9 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1224 | 87 |
| low | 0.1912 | 73 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2144 | 108 |
| short_horizon | 0.0364 | 28 |
| medium_horizon | 0.0194 | 18 |
| category_diverse | 0.0296 | 7 |
| top_volume | 0.1343 | 6 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1348
- Mean Brier: 0.0810
- Trust vs Brier correlation: -0.2571 (n=1348)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0073 | 0.5900 | 5 |
| v0.2 | 0.0885 | -0.3164 | 1516 |
