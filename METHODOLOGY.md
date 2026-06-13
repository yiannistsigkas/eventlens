# EventLens Methodology

> Pre-registered 2026-06-13, before any non-empty Brier validation results
> existed (`data/validation/brier_rows.json` had `n_rows = 0` at commit time).
> The validation plan below is frozen; changes to it after outcome data exists
> must be documented as amendments, not silent edits.

## Project thesis

EventLens evaluates whether prediction-market prices should be trusted as
probabilities. The core hypothesis is:

> Markets with lower ex-ante EventLens trust scores will exhibit higher
> ex-post Brier error after resolution.

EventLens does not attempt to beat market prices. It measures market quality
using liquidity, concentration, resolution clarity, and category calibration.

---

## Score-version discipline

All scored rows include a `score_version`.

Historical scores are never overwritten. If the scoring formula changes, a
new score version is created.

The primary validation for a score version uses only the scores produced by
that version at the time of observation.

Historical rows may be re-scored only in a separate robustness analysis with
a new score-version label. Score versions are never retroactively overwritten.

---

## Ex-ante / ex-post firewall

Trust scores are computed before resolution.

Final outcomes, Brier errors, and resolved-market data are not used as inputs
to the trust score for an active market. (The category-calibration component
uses only markets already resolved before the scored snapshot; see below.)

The scoring pipeline (`scripts/score_markets.py`) and the validation pipeline
(`scripts/resolution_tracker.py`, `scripts/validation_report.py`) are
separated by design: outcomes live only under `data/validation/`.

---

## Validation eligibility

A snapshot is validation-eligible only if:

1. the market has a valid market ID;
2. the market has a valid price;
3. the snapshot was observed before the market deadline;
4. the market has binary outcome labels;
5. the market has enough metadata to map the final outcome to the scored
   outcome;
6. the row is not marked as expired/unresolved at observation time.

Rows failing eligibility remain in the append-only logs but are excluded from
headline validation. Eligibility reasons are recorded per row
(`validation_ineligible_reasons`).

---

## Primary snapshot-selection rule

For each resolved market, the primary validation snapshot is:

> the latest validation-eligible snapshot observed at least 24 hours before
> the market `end_date` or official resolution timestamp, whichever is
> earlier/available.

If no such snapshot exists, the market is excluded from the primary headline
validation and included only in a separate short-horizon/same-day descriptive
analysis.

Rationale: this avoids last-minute price collapse contaminating the test,
avoids cherry-picking among multiple daily snapshots, and still reflects a
realistic "what did we know before resolution?" view. It also prevents
same-day sports markets from dominating the headline chart.

This rule is fixed before any non-empty Brier results exist.

---

## Outcome and Brier calculation

For each resolved binary market:

    Brier error = (p - y)^2

Where:

* `p` is the market-implied probability of the scored outcome at the selected
  snapshot;
* `y = 1` if the scored outcome resolves true;
* `y = 0` if the scored outcome resolves false.

---

## Primary validation analysis

The primary analysis is market-level. Each resolved market contributes one
snapshot selected by the primary snapshot-selection rule.

* Outcome: Brier error = `(snapshot_price - final_outcome)^2`.
* Predictor: `composite_trust_score`.
* Expected relationship: lower trust score → higher Brier error.

The primary output is a chart of trust score versus realized Brier error,
with binned averages by trust-score bucket.

---

## Evidence thresholds

EventLens will use the following interpretation thresholds:

| Resolved markets                  | Interpretation                     |
| --------------------------------: | ---------------------------------- |
| fewer than 30                     | No validation claim                |
| 30–99                             | Early descriptive evidence only    |
| 100–299                           | Preliminary validation             |
| 300+ across at least 4 categories | Stronger cross-category validation |

The first 30 resolved markets are expected to be biased toward short-horizon
sports and crypto markets. Any early result will be labelled as short-horizon
descriptive evidence, not full validation.

---

## Robustness checks

The validation report will include:

1. primary market-level analysis;
2. all-snapshots analysis with market-level clustering;
3. results excluding rows where `spread_is_missing = true`;
4. results excluding same-day markets;
5. results by horizon bucket;
6. results by category;
7. composite score excluding category calibration;
8. each subscore alone:
   * liquidity score;
   * concentration score;
   * resolution clarity score;
   * category calibration score;
9. results by `score_version` (v0.2 only for the primary analysis, unless
   explicitly comparing score versions).

---

## Category calibration rule

Category calibration uses only resolved markets available before the scored
snapshot.

Early category calibration is shrinkage-weighted (`n / (n + 50)`) toward a
global prior and marked as low-confidence until sufficient resolved
observations exist.

Validation will be reported both with and without the category-calibration
component.

---

## Missing-spread handling

Rows with missing spread are retained but flagged via `spread_is_missing`.

The primary validation includes these rows unless they fail validation
eligibility. A robustness check excludes all missing-spread rows, since
one-sided books may themselves indicate poor market quality.

---

## Shadow-mode LLM resolution analyzer

An LLM-based resolution-risk analyzer may run in shadow mode.

Shadow-mode outputs are logged (`keyword_resolution_score`,
`llm_resolution_score_shadow`, and their difference) but do not enter the
v0.2 composite trust score.

Any future inclusion of the LLM score in the composite requires a new
`score_version`.

---

## Collection breadth change (2026-06-13)

Beginning 2026-06-13, while `brier_rows = 0`, EventLens widened the daily
scored universe from ~100 to ~300 active markets. This affects *which* markets
are observed; it does **not** change the scoring formula, `score_version`, the
validation eligibility rule, or the primary snapshot rule.

Rationale: the validation timeline is gated by unique resolved-market count,
not snapshot count, and unobserved snapshots are permanently unrecoverable.
A wider, fast-resolving sample accelerates the only real bottleneck.

This is recorded as a **collection-policy change**, separate from scoring:

- `collection_policy_version` answers *why a market was observed* (breadth);
  `score_version` answers *how it was scored* (the frozen formula). The two
  move independently. The current values are
  `collection_policy_version = "v0.2-wide-300"` and `score_version = v0.2`.
- The scored sample is stratified (~300 after dedup): `top_volume` 75,
  `short_horizon` 75, `medium_horizon` 50, `low_liquidity` 50,
  `category_diverse` 50. Buckets are tilted toward fast-resolving markets;
  `low_liquidity` deliberately retains the thin tail the score must flag.
- A wider net pulls in more thin, barely-traded markets. Every row therefore
  carries data-quality metadata so validation can stratify rather than let the
  thin tail dominate: `data_quality_tier` (high/medium/low),
  `volume_rank_at_fetch`, `sample_bucket`, `spread_is_missing`,
  `spread_missing_reason`, `concentration_is_placeholder`,
  `orderbook_available`, `holders_available`.
- A cheap Tier-1 metadata archive (`data/metadata_archive/`) records slim
  book-free metadata for the active-market universe each run (top ~1200 by
  volume), preserving knowledge of the daily universe and supplying the global
  `volume_rank_at_fetch`. Scored markets below that depth carry a null rank,
  which itself reads as "deep volume tail".

If missing-spread or placeholder rates rise with the wider net, the response
is to preserve and stratify the data, not to shrink the sample — thin markets
are part of the thesis. Validation can be run on all rows, on high-data-quality
rows only, excluding missing-spread rows, and by collection bucket / volume
rank / horizon.

---

## Current frozen version

The current frozen methodology is:

    score_version = v0.2
    collection_policy_version = v0.2-wide-300

The scoring formula was frozen, and this document first committed, before any
non-empty Brier validation results existed. The 2026-06-13 collection-breadth
change widened observation only; it left the scoring formula untouched.
