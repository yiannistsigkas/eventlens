# EventLens Validation Report

Generated: `2026-07-14T12:35:33Z`

- Brier rows: 3410
- Eligible Brier rows: 3410
- Unique resolved markets: 2220
- Primary analysis rows: 377
- Markets excluded from primary (no 24h-prior snapshot): 1843
- Mean Brier: 0.1282
- Trust vs Brier correlation: -0.5829 (n=377)
- Trust vs Brier excluding missing spreads: -0.4877 (n=248)
- Trust vs Brier high-data-quality only: -0.4889 (n=240)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2144 | 75 |
| 40-55 | 0.1754 | 158 |
| 55-70 | 0.0379 | 118 |
| 70-85 | 0.0031 | 25 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1625 | 219 |
| 8-30d | 0.0764 | 129 |
| 31-90d | 0.0853 | 23 |
| 90d+ | 0.1775 | 5 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1490 | 193 |
| Weather | 0.0297 | 27 |
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
| Culture | 0.1756 | 4 |
| Formula 1 | 0.2293 | 4 |
| Privates | 0.2318 | 4 |
| ice hockey | 0.0001 | 4 |
| Celebrities | 0.1623 | 3 |
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
| ATP | 0.2704 | 1 |
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
| news_event | 0.0988 | 161 |
| sports_outcome | 0.0925 | 115 |
| sports_prop | 0.2346 | 76 |
| crypto_price | 0.1636 | 21 |
| election | 0.1649 | 3 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1085 | 240 |
| low | 0.1641 | 127 |
| Unknown | 0.1213 | 8 |
| medium | 0.2401 | 2 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2141 | 203 |
| medium_horizon | 0.0379 | 65 |
| top_volume | 0.0193 | 43 |
| short_horizon | 0.0352 | 38 |
| category_diverse | 0.0082 | 27 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1843
- Mean Brier: 0.0932
- Trust vs Brier correlation: -0.2415 (n=1843)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0015 | 0.3822 | 35 |
| v0.2 | 0.0989 | -0.3168 | 2220 |
