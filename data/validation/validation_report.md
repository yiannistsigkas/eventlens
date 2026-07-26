# EventLens Validation Report

Generated: `2026-07-26T11:50:28Z`

- Brier rows: 5063
- Eligible Brier rows: 5063
- Unique resolved markets: 3384
- Primary analysis rows: 662
- Markets excluded from primary (no 24h-prior snapshot): 2722
- Mean Brier: 0.1245
- Trust vs Brier correlation: -0.4417 (n=662)
- Trust vs Brier excluding missing spreads: -0.3748 (n=518)
- Trust vs Brier high-data-quality only: -0.3739 (n=509)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2120 | 98 |
| 40-55 | 0.1589 | 316 |
| 55-70 | 0.0484 | 209 |
| 70-85 | 0.0356 | 38 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1651 | 298 |
| 8-30d | 0.1056 | 186 |
| 31-90d | 0.0732 | 170 |
| 90d+ | 0.1600 | 7 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1499 | 242 |
| Soccer | 0.0642 | 58 |
| Weather | 0.0287 | 39 |
| Economy | 0.0818 | 25 |
| 2026 FIFA World Cup | 0.0522 | 21 |
| CPI | 0.0614 | 21 |
| FIFA World Cup | 0.0305 | 11 |
| Awards | 0.0883 | 10 |
| Culture | 0.2095 | 10 |
| Macro Indicators | 0.1532 | 10 |
| Politics | 0.0972 | 10 |
| Formula 1 | 0.1839 | 9 |
| MLB | 0.1860 | 9 |
| Solana | 0.1576 | 9 |
| banks | 0.0937 | 9 |
| Tech | 0.1949 | 8 |
| Finance | 0.2919 | 7 |
| Iran | 0.0561 | 7 |
| Tennis | 0.2704 | 7 |
| Business | 0.0000 | 6 |
| Inflation | 0.1168 | 6 |
| Recurring | 0.1349 | 6 |
| Bank of America | 0.0347 | 5 |
| Banking | 0.2081 | 5 |
| Economic Policy | 0.0000 | 5 |
| Elon | 0.2188 | 5 |
| Morgan Stanley | 0.2314 | 5 |
| NFLX | 0.1321 | 5 |
| XRP | 0.1489 | 5 |
| AI | 0.0690 | 4 |
| OPEN | 0.2407 | 4 |
| Privates | 0.2318 | 4 |
| Trump | 0.2172 | 4 |
| ice hockey | 0.0001 | 4 |
| CS2 | 0.2502 | 3 |
| Celebrities | 0.1623 | 3 |
| FIFA | 0.1723 | 3 |
| IBKR | 0.1672 | 3 |
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
| IBM | 0.0484 | 1 |
| INTC | 0.1225 | 1 |
| JNJ | 0.2256 | 1 |
| LA Mayor | 0.0020 | 1 |
| Middle East | 0.2070 | 1 |
| Monthly | 0.2271 | 1 |
| NBA | 0.2328 | 1 |
| NVDA | 0.1486 | 1 |
| RTX | 0.0036 | 1 |
| Rugby Top 14 | 0.2809 | 1 |
| Soccer Transfers | 0.2401 | 1 |
| TV | 0.1560 | 1 |
| World | 0.0000 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1070 | 386 |
| sports_outcome | 0.1105 | 162 |
| sports_prop | 0.2348 | 77 |
| crypto_price | 0.1636 | 25 |
| election | 0.0947 | 11 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1155 | 509 |
| low | 0.1546 | 142 |
| Unknown | 0.1213 | 8 |
| medium | 0.2434 | 3 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2123 | 297 |
| medium_horizon | 0.0634 | 229 |
| short_horizon | 0.0331 | 50 |
| top_volume | 0.0288 | 47 |
| category_diverse | 0.0483 | 38 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 2722
- Mean Brier: 0.1041
- Trust vs Brier correlation: -0.2278 (n=2722)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0208 | 0.4092 | 37 |
| v0.2 | 0.1078 | -0.2777 | 3384 |
