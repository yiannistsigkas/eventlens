# EventLens Validation Report

Generated: `2026-08-03T15:41:34Z`

- Brier rows: 6400
- Eligible Brier rows: 6400
- Unique resolved markets: 4188
- Primary analysis rows: 918
- Markets excluded from primary (no 24h-prior snapshot): 3270
- Mean Brier: 0.1245
- Trust vs Brier correlation: -0.4034 (n=918)
- Trust vs Brier excluding missing spreads: -0.3845 (n=713)
- Trust vs Brier high-data-quality only: -0.3838 (n=703)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2097 | 132 |
| 40-55 | 0.1451 | 496 |
| 55-70 | 0.0544 | 243 |
| 70-85 | 0.0328 | 44 |
| 85-100 | 0.0140 | 3 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1715 | 379 |
| 31-90d | 0.0623 | 272 |
| 8-30d | 0.1221 | 251 |
| 90d+ | 0.1131 | 15 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1330 | 323 |
| Soccer | 0.0642 | 58 |
| Weather | 0.0564 | 41 |
| Economy | 0.0683 | 30 |
| Tour de France | 0.0131 | 29 |
| Solana | 0.1961 | 26 |
| 2026 FIFA World Cup | 0.0522 | 21 |
| CPI | 0.0614 | 21 |
| Culture | 0.2336 | 21 |
| Macro Indicators | 0.1119 | 18 |
| Politics | 0.0667 | 16 |
| Trump | 0.1536 | 15 |
| Tech | 0.1985 | 14 |
| Finance | 0.2536 | 12 |
| FIFA World Cup | 0.0305 | 11 |
| Awards | 0.0883 | 10 |
| Elon | 0.2354 | 10 |
| Formula 1 | 0.1839 | 9 |
| Iran | 0.0436 | 9 |
| MLB | 0.1860 | 9 |
| banks | 0.0937 | 9 |
| NBA | 0.0867 | 8 |
| Movies | 0.1688 | 7 |
| Tennis | 0.2704 | 7 |
| Business | 0.0000 | 6 |
| Inflation | 0.1168 | 6 |
| Recurring | 0.1349 | 6 |
| Rewards 20, 4.5, 50 | 0.1378 | 6 |
| XRP | 0.1242 | 6 |
| AI | 0.0783 | 5 |
| Bank of America | 0.0347 | 5 |
| Banking | 0.2081 | 5 |
| Economic Policy | 0.0000 | 5 |
| Fed Rates | 0.2421 | 5 |
| Morgan Stanley | 0.2314 | 5 |
| NFLX | 0.1321 | 5 |
| AAPL | 0.1693 | 4 |
| CS2 | 0.2540 | 4 |
| KPIs | 0.2048 | 4 |
| MSFT | 0.1780 | 4 |
| OPEN | 0.2407 | 4 |
| Privates | 0.2318 | 4 |
| TSLA | 0.3645 | 4 |
| ice hockey | 0.0001 | 4 |
| AMZN | 0.2396 | 3 |
| Celebrities | 0.1623 | 3 |
| FIFA | 0.1723 | 3 |
| Fed | 0.0206 | 3 |
| GDP | 0.0861 | 3 |
| IBKR | 0.1672 | 3 |
| Major League Pickleball | 0.2246 | 3 |
| NVDA | 0.2093 | 3 |
| Oil | 0.0000 | 3 |
| South Korea | 0.0468 | 3 |
| TV | 0.2088 | 3 |
| BTS | 0.1972 | 2 |
| Bitcoin | 0.0055 | 2 |
| Cook | 0.2391 | 2 |
| Crypto | 0.2312 | 2 |
| Crypto Prices | 0.3271 | 2 |
| Games | 0.2256 | 2 |
| Geopolitics | 0.0001 | 2 |
| Lambda | 0.2050 | 2 |
| Monthly | 0.1783 | 2 |
| Musk v Altman | 0.2359 | 2 |
| Pickleball | 0.1225 | 2 |
| Trump-Netanyahu | 0.2011 | 2 |
| UFC | 0.1445 | 2 |
| WFC | 0.2403 | 2 |
| fraud | 0.1225 | 2 |
| transit | 0.0009 | 2 |
| ABBV | 0.0010 | 1 |
| AQI | 0.2209 | 1 |
| ATP | 0.2704 | 1 |
| Claude | 0.0361 | 1 |
| Glean | 0.0841 | 1 |
| Head coach | 0.1806 | 1 |
| Hide From New | 0.2256 | 1 |
| Highest temperature | 0.0000 | 1 |
| Hunter Biden | 0.0001 | 1 |
| IBM | 0.0484 | 1 |
| INTC | 0.1225 | 1 |
| JNJ | 0.2256 | 1 |
| LA Mayor | 0.0020 | 1 |
| M&A | 0.3249 | 1 |
| MU | 0.2209 | 1 |
| Meta | 0.2601 | 1 |
| Middle East | 0.2070 | 1 |
| RTX | 0.0036 | 1 |
| Rugby Top 14 | 0.2809 | 1 |
| Soccer Transfers | 0.2401 | 1 |
| World | 0.0000 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1156 | 536 |
| sports_outcome | 0.0993 | 240 |
| sports_prop | 0.2316 | 80 |
| crypto_price | 0.1758 | 45 |
| election | 0.1284 | 16 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1247 | 703 |
| low | 0.1217 | 203 |
| Unknown | 0.1213 | 8 |
| medium | 0.2450 | 4 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2047 | 433 |
| medium_horizon | 0.0572 | 329 |
| short_horizon | 0.0528 | 54 |
| top_volume | 0.0277 | 52 |
| category_diverse | 0.0518 | 49 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 3270
- Mean Brier: 0.1064
- Trust vs Brier correlation: -0.2313 (n=3270)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0208 | 0.4092 | 37 |
| v0.2 | 0.1100 | -0.2771 | 4188 |
