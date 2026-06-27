# EventLens Validation Report

Generated: `2026-06-27T14:07:40Z`

- Brier rows: 1881
- Eligible Brier rows: 1881
- Unique resolved markets: 1636
- Primary analysis rows: 189
- Markets excluded from primary (no 24h-prior snapshot): 1447
- Mean Brier: 0.1498
- Trust vs Brier correlation: -0.5099 (n=189)
- Trust vs Brier excluding missing spreads: -0.3446 (n=103)
- Trust vs Brier high-data-quality only: -0.3446 (n=97)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2140 | 49 |
| 40-55 | 0.1901 | 79 |
| 55-70 | 0.0529 | 52 |
| 70-85 | 0.0068 | 8 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1735 | 136 |
| 8-30d | 0.0945 | 42 |
| 31-90d | 0.0591 | 9 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1914 | 115 |
| Weather | 0.0321 | 25 |
| 2026 FIFA World Cup | 0.0233 | 7 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2426 | 4 |
| Formula 1 | 0.2293 | 4 |
| Recurring | 0.0789 | 4 |
| ice hockey | 0.0001 | 4 |
| Politics | 0.2746 | 3 |
| XRP | 0.1072 | 3 |
| FIFA World Cup | 0.0003 | 2 |
| Soccer | 0.1352 | 2 |
| Solana | 0.1443 | 2 |
| UFC | 0.1445 | 2 |
| Head coach | 0.1806 | 1 |
| Hide From New | 0.2256 | 1 |
| Highest temperature | 0.0000 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| le mans | 0.2070 | 1 |
| transit | 0.0000 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| sports_prop | 0.2336 | 67 |
| news_event | 0.0827 | 65 |
| sports_outcome | 0.1346 | 47 |
| crypto_price | 0.1029 | 9 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1162 | 97 |
| low | 0.1914 | 84 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2163 | 119 |
| short_horizon | 0.0374 | 29 |
| medium_horizon | 0.0185 | 24 |
| top_volume | 0.0895 | 9 |
| category_diverse | 0.0296 | 7 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1447
- Mean Brier: 0.0876
- Trust vs Brier correlation: -0.2567 (n=1447)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0046 | 0.6063 | 8 |
| v0.2 | 0.0944 | -0.3147 | 1636 |
