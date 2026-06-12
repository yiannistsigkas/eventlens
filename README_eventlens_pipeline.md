# EventLens v0.2 pipeline (Polymarket)

## Setup
    pip install requests
    mkdir -p data/raw data/processed data/debug data/validation scripts

## Run (daily, manually or via cron)
    python scripts/fetch_polymarket_markets.py
    python scripts/score_markets.py
    python scripts/resolution_tracker.py
    python scripts/validation_report.py

## Sampling (v0.2 — sample for validation, not just volume)
Top-volume-only sampling yields liquid but slow-resolving markets that starve
the Brier validation loop. The fetcher builds a stratified sample instead:

| Bucket            | n  | Purpose                                  |
| ----------------- | -- | ---------------------------------------- |
| top_volume        | 30 | High-quality/liquid benchmark            |
| short_horizon     | 30 | Soonest-ending (≤30d) — fast validation  |
| low_liquidity     | 20 | Thin books — stress-test trust score     |
| category_diverse  | 20 | Avoid Sports/Politics dominance          |

Deduplicated by market_id; each row carries `sample_bucket`.

## Outputs
- data/raw/raw_snapshot_<ts>.json        — exact market state as observed (append-only)
- data/processed/snapshots.jsonl         — one scored row per market per run (append-only)
- data/scored_markets.json               — latest scores for the dashboard (a view)
- data/debug/                            — samples of unexpected API responses
- data/validation/resolutions.jsonl      — detected market outcomes (append-only)
- data/validation/brier_rows.json        — ex-ante snapshot × outcome joins (regenerated view)
- data/validation/calibration_table.json — per-category Brier stats feeding scoring (regenerated view)
- data/validation/validation_report.json — trust-vs-Brier metrics and grouped cuts
- data/validation/validation_report.md   — human-readable thesis tables
- data/validation/trust_vs_brier.svg     — scatter/fit chart once ≥2 markets resolve

## Methodology rules (do not break these)
1. Scores are ex-ante: computed and timestamped strictly before resolution.
   Final outcomes and Brier errors never enter scoring inputs. Outcomes live
   in data/validation/ only; a Brier row requires observed_at < closed_time.
2. Nothing historical is overwritten. Formula changes increment score_version
   (v0.2 = stronger resolution heuristic + horizon fields).
3. Placeholders and gaps are explicit (concentration_is_placeholder,
   spread_is_missing, resolution_llm_analyzed=False).
4. Category calibration uses shrinkage (n/(n+50)) toward a global prior and
   reports confidence; the table is rebuilt from real resolved markets by
   resolution_tracker.py (one observation per market: its latest pre-close
   snapshot).

## Row fields added in v0.2
- sample_bucket, days_to_resolution, horizon_bucket (0-7d / 8-30d / 31-90d / 90d+),
  spread_is_missing

## Metadata patch v0.2.1
- validation_eligible plus stable ineligibility reason codes
- market_type (sports_prop, sports_outcome, crypto_price, election, etc.)
- binary outcome labels retained so Up/Down and Over/Under markets are not
  mislabeled as literal Yes/No
- structured resolution flags; composite score weights and penalties unchanged,
  so score_version remains v0.2

## Validation report
Primary tables use the latest validation-eligible pre-close snapshot per
resolved market. This prevents frequently sampled markets from dominating
mean Brier and correlation estimates. Score-version cuts retain one latest
snapshot per market per version.

## Resolution heuristic v0.2
Asks "can this resolve cleanly under plausible edge cases?", not just "is
there a source?". New flags: unverifiable/metaphysical subject matter,
subjective-consensus resolution wording, deep longshot (<1c) with distant
deadline. LLM analyzer (same penalty schema) is still ahead.

## Diagnostics tripwires (printed by score_markets.py)
- trust stdev < 8            — scores may lack discriminating power
- resolution stdev = 0       — heuristic not discriminating
- >70% resolve after 180d    — validation will be slow
- >50% from one category     — sample too homogeneous

## Roadmap
- accumulate short-horizon ex-ante snapshots; target 100–300 resolved
  within weeks for the first trust-vs-Brier read
- validation cuts: trust-vs-Brier with and without spread_is_missing rows,
  and per horizon_bucket
- LLM resolution analyzer replacing the keyword heuristic (same schema)
- wallet-level concentration from on-chain OrderFilled events (do not infer
  trade direction from the public book feed)
- only then: wire the dashboard to real JSON
