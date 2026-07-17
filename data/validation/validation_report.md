# EventLens Validation Report

Generated: `2026-07-17T08:11:20Z`

- Brier rows: 3757
- Eligible Brier rows: 3757
- Unique resolved markets: 2447
- Primary analysis rows: 470
- Markets excluded from primary (no 24h-prior snapshot): 1977
- Mean Brier: 0.1273
- Trust vs Brier correlation: -0.4962 (n=470)
- Trust vs Brier excluding missing spreads: -0.4081 (n=337)
- Trust vs Brier high-data-quality only: -0.4069 (n=328)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2148 | 77 |
| 40-55 | 0.1751 | 200 |
| 55-70 | 0.0488 | 164 |
| 70-85 | 0.0099 | 28 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1611 | 234 |
| 8-30d | 0.0840 | 146 |
| 31-90d | 0.1050 | 83 |
| 90d+ | 0.1867 | 6 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1498 | 199 |
| Weather | 0.0271 | 31 |
| CPI | 0.0614 | 21 |
| 2026 FIFA World Cup | 0.0304 | 14 |
| Soccer | 0.0889 | 14 |
| FIFA World Cup | 0.0305 | 11 |
| Macro Indicators | 0.1532 | 10 |
| MLB | 0.1860 | 9 |
| banks | 0.0937 | 9 |
| Tech | 0.1949 | 8 |
| Business | 0.0000 | 6 |
| Finance | 0.2980 | 6 |
| Iran | 0.0537 | 6 |
| Politics | 0.1618 | 6 |
| Recurring | 0.1349 | 6 |
| Solana | 0.1346 | 6 |
| Bank of America | 0.0347 | 5 |
| Banking | 0.2081 | 5 |
| Culture | 0.1905 | 5 |
| Economic Policy | 0.0000 | 5 |
| Economy | 0.0010 | 5 |
| Morgan Stanley | 0.2314 | 5 |
| XRP | 0.1489 | 5 |
| AI | 0.0690 | 4 |
| Formula 1 | 0.2293 | 4 |
| Privates | 0.2318 | 4 |
| Tennis | 0.2964 | 4 |
| Trump | 0.2172 | 4 |
| ice hockey | 0.0001 | 4 |
| Celebrities | 0.1623 | 3 |
| KPIs | 0.2671 | 3 |
| Oil | 0.0000 | 3 |
| South Korea | 0.0468 | 3 |
| Cook | 0.2391 | 2 |
| Crypto | 0.2312 | 2 |
| Crypto Prices | 0.3271 | 2 |
| Geopolitics | 0.0001 | 2 |
| MSFT | 0.1183 | 2 |
| Major League Pickleball | 0.2401 | 2 |
| UFC | 0.1445 | 2 |
| WFC | 0.2403 | 2 |
| fraud | 0.1225 | 2 |
| transit | 0.0009 | 2 |
| AAPL | 0.0064 | 1 |
| AMZN | 0.2381 | 1 |
| ATP | 0.2704 | 1 |
| Bitcoin | 0.0000 | 1 |
| Claude | 0.0361 | 1 |
| Head coach | 0.1806 | 1 |
| Hide From New | 0.2256 | 1 |
| Highest temperature | 0.0000 | 1 |
| JNJ | 0.2256 | 1 |
| LA Mayor | 0.0020 | 1 |
| Middle East | 0.2070 | 1 |
| Monthly | 0.2271 | 1 |
| NBA | 0.2328 | 1 |
| Rugby Top 14 | 0.2809 | 1 |
| Soccer Transfers | 0.2401 | 1 |
| World | 0.0000 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1069 | 246 |
| sports_outcome | 0.0967 | 121 |
| sports_prop | 0.2346 | 76 |
| crypto_price | 0.1581 | 22 |
| election | 0.1241 | 4 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1131 | 328 |
| low | 0.1607 | 131 |
| Unknown | 0.1213 | 8 |
| medium | 0.2434 | 3 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2141 | 224 |
| medium_horizon | 0.0710 | 130 |
| top_volume | 0.0228 | 45 |
| short_horizon | 0.0327 | 42 |
| category_diverse | 0.0080 | 28 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1977
- Mean Brier: 0.0947
- Trust vs Brier correlation: -0.2440 (n=1977)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0022 | 0.4414 | 36 |
| v0.2 | 0.1007 | -0.3088 | 2447 |
