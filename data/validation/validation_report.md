# EventLens Validation Report

Generated: `2026-07-21T07:04:52Z`

- Brier rows: 4393
- Eligible Brier rows: 4393
- Unique resolved markets: 2864
- Primary analysis rows: 560
- Markets excluded from primary (no 24h-prior snapshot): 2304
- Mean Brier: 0.1252
- Trust vs Brier correlation: -0.4466 (n=560)
- Trust vs Brier excluding missing spreads: -0.3612 (n=423)
- Trust vs Brier high-data-quality only: -0.3598 (n=414)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2145 | 85 |
| 40-55 | 0.1608 | 255 |
| 55-70 | 0.0526 | 183 |
| 70-85 | 0.0356 | 36 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1646 | 265 |
| 8-30d | 0.0987 | 160 |
| 31-90d | 0.0754 | 127 |
| 90d+ | 0.1600 | 7 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1550 | 215 |
| Soccer | 0.0642 | 58 |
| Weather | 0.0256 | 33 |
| 2026 FIFA World Cup | 0.0522 | 21 |
| CPI | 0.0614 | 21 |
| FIFA World Cup | 0.0305 | 11 |
| Macro Indicators | 0.1532 | 10 |
| Culture | 0.2077 | 9 |
| MLB | 0.1860 | 9 |
| banks | 0.0937 | 9 |
| Tech | 0.1949 | 8 |
| Formula 1 | 0.1785 | 7 |
| Politics | 0.1387 | 7 |
| Solana | 0.1376 | 7 |
| Business | 0.0000 | 6 |
| Finance | 0.2980 | 6 |
| Iran | 0.0537 | 6 |
| Recurring | 0.1349 | 6 |
| Bank of America | 0.0347 | 5 |
| Banking | 0.2081 | 5 |
| Economic Policy | 0.0000 | 5 |
| Economy | 0.0010 | 5 |
| Elon | 0.2188 | 5 |
| Morgan Stanley | 0.2314 | 5 |
| XRP | 0.1489 | 5 |
| AI | 0.0690 | 4 |
| Privates | 0.2318 | 4 |
| Tennis | 0.2964 | 4 |
| Trump | 0.2172 | 4 |
| ice hockey | 0.0001 | 4 |
| Celebrities | 0.1623 | 3 |
| FIFA | 0.1723 | 3 |
| KPIs | 0.2671 | 3 |
| Oil | 0.0000 | 3 |
| South Korea | 0.0468 | 3 |
| BTS | 0.1972 | 2 |
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
| AQI | 0.2209 | 1 |
| ATP | 0.2704 | 1 |
| Bitcoin | 0.0000 | 1 |
| Claude | 0.0361 | 1 |
| Head coach | 0.1806 | 1 |
| Hide From New | 0.2256 | 1 |
| Highest temperature | 0.0000 | 1 |
| Hunter Biden | 0.0001 | 1 |
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
| news_event | 0.1025 | 316 |
| sports_outcome | 0.1119 | 136 |
| sports_prop | 0.2346 | 76 |
| crypto_price | 0.1580 | 23 |
| election | 0.1301 | 8 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1133 | 414 |
| low | 0.1596 | 135 |
| Unknown | 0.1213 | 8 |
| medium | 0.2434 | 3 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2154 | 254 |
| medium_horizon | 0.0616 | 177 |
| top_volume | 0.0288 | 47 |
| short_horizon | 0.0313 | 44 |
| category_diverse | 0.0477 | 37 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 2304
- Mean Brier: 0.0973
- Trust vs Brier correlation: -0.2396 (n=2304)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0208 | 0.4092 | 37 |
| v0.2 | 0.1023 | -0.2952 | 2864 |
