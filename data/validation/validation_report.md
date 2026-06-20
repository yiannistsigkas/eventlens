# EventLens Validation Report

Generated: `2026-06-20T13:08:38Z`

- Brier rows: 968
- Eligible Brier rows: 968
- Unique resolved markets: 854
- Primary analysis rows: 67
- Markets excluded from primary (no 24h-prior snapshot): 787
- Mean Brier: 0.1553
- Trust vs Brier correlation: -0.3249 (n=67)
- Trust vs Brier excluding missing spreads: -0.2416 (n=47)
- Trust vs Brier high-data-quality only: -0.2349 (n=41)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1910 | 5 |
| 40-55 | 0.2100 | 36 |
| 55-70 | 0.0926 | 20 |
| 70-85 | 0.0073 | 5 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1682 | 55 |
| 31-90d | 0.0457 | 7 |
| 8-30d | 0.2040 | 3 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2449 | 21 |
| Weather | 0.0001 | 9 |
| Economic Policy | 0.0000 | 5 |
| Finance | 0.2426 | 4 |
| Formula 1 | 0.2293 | 4 |
| Recurring | 0.0789 | 4 |
| ice hockey | 0.0001 | 4 |
| Politics | 0.2746 | 3 |
| Solana | 0.1443 | 2 |
| UFC | 0.1445 | 2 |
| XRP | 0.1558 | 2 |
| 2026 FIFA World Cup | 0.1564 | 1 |
| FIFA World Cup | 0.0005 | 1 |
| Head coach | 0.1806 | 1 |
| Iran | 0.3192 | 1 |
| Middle East | 0.2070 | 1 |
| Soccer | 0.2704 | 1 |
| le mans | 0.2070 | 1 |

## Market Types

| Market type | Mean Brier | n |
| --- | --- | --- |
| news_event | 0.1143 | 38 |
| sports_prop | 0.2898 | 13 |
| crypto_price | 0.1145 | 8 |
| sports_outcome | 0.1914 | 7 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1615 | 41 |
| low | 0.1561 | 18 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2187 | 40 |
| short_horizon | 0.0237 | 12 |
| category_diverse | 0.0345 | 6 |
| medium_horizon | 0.0533 | 6 |
| top_volume | 0.4028 | 2 |
| Unknown | 0.0363 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 787
- Mean Brier: 0.0810
- Trust vs Brier correlation: -0.2388 (n=787)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0182 | N/A | 2 |
| v0.2 | 0.0860 | -0.2667 | 854 |
