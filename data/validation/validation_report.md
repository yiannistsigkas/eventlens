# EventLens Validation Report

Generated: `2026-07-10T14:09:24Z`

- Brier rows: 3182
- Eligible Brier rows: 3182
- Unique resolved markets: 2054
- Primary analysis rows: 351
- Markets excluded from primary (no 24h-prior snapshot): 1703
- Mean Brier: 0.1257
- Trust vs Brier correlation: -0.5925 (n=351)
- Trust vs Brier excluding missing spreads: -0.4855 (n=224)
- Trust vs Brier high-data-quality only: -0.4866 (n=216)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.2150 | 66 |
| 40-55 | 0.1750 | 149 |
| 55-70 | 0.0335 | 113 |
| 70-85 | 0.0033 | 22 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1618 | 205 |
| 8-30d | 0.0726 | 120 |
| 31-90d | 0.0853 | 23 |
| 90d+ | 0.1268 | 2 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.1511 | 186 |
| Weather | 0.0321 | 25 |
| 2026 FIFA World Cup | 0.0318 | 13 |
| Soccer | 0.0483 | 12 |
| FIFA World Cup | 0.0305 | 11 |
| Tech | 0.1879 | 7 |
| Business | 0.0000 | 6 |
| Politics | 0.1618 | 6 |
| Recurring | 0.1349 | 6 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2421 | 5 |
| Iran | 0.0639 | 5 |
| XRP | 0.1489 | 5 |
| Formula 1 | 0.2293 | 4 |
| Privates | 0.2318 | 4 |
| Solana | 0.1310 | 4 |
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
| Bitcoin | 0.0000 | 1 |
| Claude | 0.0361 | 1 |
| Culture | 0.0083 | 1 |
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
| news_event | 0.0881 | 143 |
| sports_outcome | 0.0925 | 108 |
| sports_prop | 0.2346 | 76 |
| crypto_price | 0.1597 | 20 |
| election | 0.1649 | 3 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1024 | 216 |
| low | 0.1645 | 125 |
| Unknown | 0.1213 | 8 |
| medium | 0.2401 | 2 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2147 | 186 |
| medium_horizon | 0.0290 | 62 |
| top_volume | 0.0206 | 40 |
| short_horizon | 0.0371 | 36 |
| category_diverse | 0.0080 | 26 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 1703
- Mean Brier: 0.0945
- Trust vs Brier correlation: -0.2407 (n=1703)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0016 | 0.3930 | 32 |
| v0.2 | 0.0995 | -0.3157 | 2054 |
