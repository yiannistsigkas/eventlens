# EventLens Validation Report

Generated: `2026-06-20T00:05:06Z`

- Brier rows: 915
- Eligible Brier rows: 915
- Unique resolved markets: 810
- Primary analysis rows: 63
- Markets excluded from primary (no 24h-prior snapshot): 747
- Mean Brier: 0.1574
- Trust vs Brier correlation: -0.3011 (n=63)
- Trust vs Brier excluding missing spreads: -0.2155 (n=45)
- Trust vs Brier high-data-quality only: -0.2065 (n=39)

Primary statistics use the latest eligible snapshot observed at least 24 hours before close/resolution (pre-registered in METHODOLOGY.md). Markets with only same-day snapshots appear in the short-horizon descriptive section, not the headline.

## Trust Buckets

| Trust bucket | Mean Brier | n |
| --- | --- | --- |
| 0-40 | 0.1778 | 4 |
| 40-55 | 0.2151 | 34 |
| 55-70 | 0.0926 | 20 |
| 70-85 | 0.0091 | 4 |
| 85-100 | 0.0000 | 1 |

## Horizon Buckets

| Horizon bucket | Mean Brier | n |
| --- | --- | --- |
| 0-7d | 0.1685 | 52 |
| 31-90d | 0.0533 | 6 |
| 8-30d | 0.2040 | 3 |
| 90d+ | 0.1806 | 1 |
| Unknown | 0.0363 | 1 |

## Categories

| Category | Mean Brier | n |
| --- | --- | --- |
| Sports | 0.2586 | 18 |
| Weather | 0.0001 | 8 |
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
| news_event | 0.1174 | 37 |
| sports_prop | 0.2981 | 11 |
| crypto_price | 0.1145 | 8 |
| sports_outcome | 0.2233 | 6 |
| Unknown | 0.0363 | 1 |

## Data-Quality Tiers

| Data-quality tier | Mean Brier | n |
| --- | --- | --- |
| high | 0.1636 | 39 |
| low | 0.1603 | 16 |
| Unknown | 0.1213 | 8 |

## Collection Buckets

| Collection bucket | Mean Brier | n |
| --- | --- | --- |
| low_liquidity | 0.2174 | 38 |
| short_horizon | 0.0258 | 11 |
| category_diverse | 0.0345 | 6 |
| medium_horizon | 0.0533 | 6 |
| Unknown | 0.0363 | 1 |
| top_volume | 0.8055 | 1 |

## Short-Horizon Descriptive (excluded from primary)

- Markets: 747
- Mean Brier: 0.0804
- Trust vs Brier correlation: -0.2426 (n=747)

These markets had no eligible snapshot at least 24 hours before close. Descriptive only — not part of the pre-registered primary validation.

## Score Versions

| Score version | Mean Brier | Trust correlation | n |
| --- | --- | --- | --- |
| v0.1 | 0.0363 | N/A | 1 |
| v0.2 | 0.0855 | -0.2680 | 810 |
