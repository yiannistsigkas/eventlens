# EventLens Validation Report

Generated: `2026-07-29T13:43:40Z`

- Brier rows: 5597
- Eligible Brier rows: 5597
- Unique resolved markets: 3735
- Primary analysis rows: 797
- Markets excluded from primary (no 24h-prior snapshot): 2938
- Mean Brier: 0.1186
- Trust vs Brier correlation: -0.3900 (n=797)
- Trust vs Brier excluding missing spreads: -0.3585 (n=596)
- Trust vs Brier high-data-quality only: -0.3579 (n=587)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2011 | 116 |
| 40-55 | 0.1394 | 420 |
| 55-70 | 0.0514 | 220 |
| 70-85 | 0.0347 | 39 |
| 85-100 | 0.0000 | 2 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1707 | 325 |
| 31-90d | 0.0575 | 233 |
| 8-30d | 0.1085 | 226 |
| 90d+ | 0.0934 | 12 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1308 | 315 |
| Soccer | 0.0642 | 58 |
| Weather | 0.0564 | 41 |
| Tour de France | 0.0131 | 29 |
| Economy | 0.0818 | 25 |
| 2026 FIFA World Cup | 0.0522 | 21 |
| CPI | 0.0614 | 21 |
| Solana | 0.2078 | 21 |
| Culture | 0.2254 | 15 |
| FIFA World Cup | 0.0305 | 11 |
| Awards | 0.0883 | 10 |
| Macro Indicators | 0.1532 | 10 |
| Politics | 0.0972 | 10 |
| Tech | 0.1617 | 10 |
| Formula 1 | 0.1839 | 9 |
| MLB | 0.1860 | 9 |
| banks | 0.0937 | 9 |
| Finance | 0.2919 | 7 |
| Iran | 0.0561 | 7 |
| Tennis | 0.2704 | 7 |
| Business | 0.0000 | 6 |
| Inflation | 0.1168 | 6 |
| NBA | 0.0388 | 6 |
| Recurring | 0.1349 | 6 |
| XRP | 0.1242 | 6 |
| Bank of America | 0.0347 | 5 |
| Banking | 0.2081 | 5 |
| Economic Policy | 0.0000 | 5 |
| Elon | 0.2188 | 5 |
| Morgan Stanley | 0.2314 | 5 |
| NFLX | 0.1321 | 5 |
| Trump | 0.2248 | 5 |
| AI | 0.0690 | 4 |
| CS2 | 0.2540 | 4 |
| OPEN | 0.2407 | 4 |
| Privates | 0.2318 | 4 |
| ice hockey | 0.0001 | 4 |
| Celebrities | 0.1623 | 3 |
| FIFA | 0.1723 | 3 |
| IBKR | 0.1672 | 3 |
| KPIs | 0.2671 | 3 |
| Oil | 0.0000 | 3 |
| South Korea | 0.0468 | 3 |
| TV | 0.2088 | 3 |
| BTS | 0.1972 | 2 |
| Cook | 0.2391 | 2 |
| Crypto | 0.2312 | 2 |
| Crypto Prices | 0.3271 | 2 |
| Geopolitics | 0.0001 | 2 |
| MSFT | 0.1183 | 2 |
| Major League Pickleball | 0.2401 | 2 |
| Movies | 0.1577 | 2 |
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
| IBM | 0.0484 | 1 |
| INTC | 0.1225 | 1 |
| JNJ | 0.2256 | 1 |
| LA Mayor | 0.0020 | 1 |
| Middle East | 0.2070 | 1 |
| Monthly | 0.2271 | 1 |
| NVDA | 0.1486 | 1 |
| RTX | 0.0036 | 1 |
| Rugby Top 14 | 0.2809 | 1 |
| Soccer Transfers | 0.2401 | 1 |
| World | 0.0000 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1043 | 434 |
| sports_outcome | 0.0976 | 234 |
| sports_prop | 0.2318 | 78 |
| crypto_price | 0.1851 | 38 |
| election | 0.1089 | 12 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1174 | 587 |
| low | 0.1202 | 199 |
| Unknown | 0.1213 | 8 |
| medium | 0.2434 | 3 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2022 | 361 |
| medium_horizon | 0.0530 | 292 |
| short_horizon | 0.0537 | 53 |
| top_volume | 0.0288 | 47 |
| category_diverse | 0.0426 | 43 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 2938
- Mean Brier: 0.1041
- Trust vs Brier correlation: -0.2347 (n=2938)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0208 | 0.4092 | 37 |
| v0.2 | 0.1069 | -0.2733 | 3735 |
