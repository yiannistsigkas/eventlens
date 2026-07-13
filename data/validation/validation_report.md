# EventLens Validation Report

Generated: `2026-07-13T09:19:15Z`

- Brier rows: 3310
- Eligible Brier rows: 3310
- Unique resolved markets: 2121
- Primary analysis rows: 373
- Markets excluded from primary (no 24h-prior snapshot): 1748
- Mean Brier: 0.1281
- Trust vs Brier correlation: -0.5807 (n=373)
- Trust vs Brier excluding missing spreads: -0.4848 (n=246)
- Trust vs Brier high-data-quality only: -0.4860 (n=238)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2144 | 75 |
| 40-55 | 0.1741 | 156 |
| 55-70 | 0.0385 | 116 |
| 70-85 | 0.0031 | 25 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1635 | 216 |
| 8-30d | 0.0764 | 129 |
| 31-90d | 0.0853 | 23 |
| 90d+ | 0.1516 | 4 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1490 | 193 |
| Weather | 0.0321 | 25 |
| 2026 FIFA World Cup | 0.0304 | 14 |
| Soccer | 0.0889 | 14 |
| FIFA World Cup | 0.0305 | 11 |
| MLB | 0.1860 | 9 |
| Tech | 0.1879 | 7 |
| Business | 0.0000 | 6 |
| Politics | 0.1618 | 6 |
| Recurring | 0.1349 | 6 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2421 | 5 |
| Iran | 0.0639 | 5 |
| Solana | 0.1527 | 5 |
| XRP | 0.1489 | 5 |
| Formula 1 | 0.2293 | 4 |
| Privates | 0.2318 | 4 |
| ice hockey | 0.0001 | 4 |
| Celebrities | 0.1623 | 3 |
| Culture | 0.1405 | 3 |
| Oil | 0.0000 | 3 |
| Tennis | 0.3119 | 3 |
| AI | 0.0171 | 2 |
| Cook | 0.2391 | 2 |
| Crypto | 0.2312 | 2 |
| Crypto Prices | 0.3271 | 2 |
| Geopolitics | 0.0001 | 2 |
| MSFT | 0.1183 | 2 |
| Major League Pickleball | 0.2401 | 2 |
| UFC | 0.1445 | 2 |
| fraud | 0.1225 | 2 |
| transit | 0.0009 | 2 |
| AAPL | 0.0064 | 1 |
| AMZN | 0.2381 | 1 |
| Bitcoin | 0.0000 | 1 |
| Claude | 0.0361 | 1 |
| Head coach | 0.1806 | 1 |
| Hide From New | 0.2256 | 1 |
| Highest temperature | 0.0000 | 1 |
| Middle East | 0.2070 | 1 |
| Monthly | 0.2271 | 1 |
| Rugby Top 14 | 0.2809 | 1 |
| Soccer Transfers | 0.2401 | 1 |
| World | 0.0000 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.0978 | 157 |
| sports_outcome | 0.0925 | 115 |
| sports_prop | 0.2346 | 76 |
| crypto_price | 0.1636 | 21 |
| election | 0.1649 | 3 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1083 | 238 |
| low | 0.1645 | 125 |
| Unknown | 0.1213 | 8 |
| medium | 0.2401 | 2 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2135 | 201 |
| medium_horizon | 0.0379 | 65 |
| top_volume | 0.0193 | 43 |
| short_horizon | 0.0371 | 36 |
| category_diverse | 0.0082 | 27 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1748
- Mean Brier: 0.0952
- Trust vs Brier correlation: -0.2392 (n=1748)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0015 | 0.3822 | 35 |
| v0.2 | 0.1007 | -0.3155 | 2121 |
