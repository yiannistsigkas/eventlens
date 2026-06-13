import os
import sys
import json
import tempfile
import unittest
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import fetch_polymarket_markets
import check_data_freshness
import resolution_tracker
import score_markets
import validation_report


class ScoreMetadataTests(unittest.TestCase):
    def test_validation_eligibility_accepts_binary_pre_deadline_row(self):
        eligible, reasons, source = score_markets.validation_eligibility(
            {
                "market_id": "1",
                "condition_id": "condition",
                "question": "Will it happen?",
                "end_date": "2026-06-14T00:00:00Z",
                "observed_at": "2026-06-13T00:00:00Z",
                "outcome_labels": ["Up", "Down"],
                "outcome_token_ids": ["a", "b"],
            },
            0.4,
        )
        self.assertTrue(eligible)
        self.assertEqual(reasons, [])
        self.assertEqual(source, "explicit_binary_metadata")

    def test_validation_eligibility_rejects_non_binary_row(self):
        eligible, reasons, _ = score_markets.validation_eligibility(
            {
                "market_id": "1",
                "condition_id": "condition",
                "question": "Who wins?",
                "end_date": "2026-06-14T00:00:00Z",
                "observed_at": "2026-06-13T00:00:00Z",
                "outcome_labels": ["A", "B", "C"],
                "outcome_token_ids": ["a", "b", "c"],
            },
            0.4,
        )
        self.assertFalse(eligible)
        self.assertIn("NOT_BINARY_OUTCOME", reasons)

    def test_expired_market_is_not_validation_eligible(self):
        eligible, reasons, _ = score_markets.validation_eligibility(
            {
                "market_id": "1",
                "condition_id": "condition",
                "question": "Already ended?",
                "end_date": "2026-06-12T00:00:00Z",
                "observed_at": "2026-06-13T00:00:00Z",
                "outcome_labels": ["Yes", "No"],
                "outcome_token_ids": ["a", "b"],
            },
            0.5,
        )
        self.assertFalse(eligible)
        self.assertIn("NOT_OBSERVED_BEFORE_DEADLINE", reasons)

    def test_expired_market_is_not_classified_short_horizon(self):
        days = score_markets.days_to_resolution("2026-06-12T00:00:00Z", "2026-06-13T00:00:00Z")
        self.assertLess(days, 0)
        self.assertEqual(score_markets.horizon_bucket(days), "expired_unresolved")
        # observed just past the deadline must not round back into 0-7d
        barely = score_markets.days_to_resolution("2026-06-13T00:00:00Z", "2026-06-13T01:00:00Z")
        self.assertEqual(score_markets.horizon_bucket(barely), "expired_unresolved")

    def test_market_type_distinguishes_sports_prop(self):
        self.assertEqual(
            score_markets.classify_market_type("Player: Home Runs O/U 1.5", "Sports"),
            "sports_prop",
        )

    def test_data_quality_tier_levels(self):
        # full two-sided book + real holders -> high
        self.assertEqual(score_markets.data_quality_tier(True, False, False), "high")
        # priced but holder data is a placeholder -> medium
        self.assertEqual(score_markets.data_quality_tier(True, False, True), "medium")
        # one-sided book (missing spread) -> low, regardless of holders
        self.assertEqual(score_markets.data_quality_tier(True, True, False), "low")
        # no usable book -> low
        self.assertEqual(score_markets.data_quality_tier(False, False, False), "low")

    def test_spread_missing_reason_distinguishes_book_states(self):
        two_sided = {
            "bids": [{"price": "0.40", "size": "10"}],
            "asks": [{"price": "0.42", "size": "10"}],
        }
        self.assertIsNone(score_markets.spread_missing_reason(two_sided))
        self.assertEqual(
            score_markets.spread_missing_reason({"bids": [], "asks": []}),
            "empty_book",
        )
        self.assertEqual(
            score_markets.spread_missing_reason(
                {"bids": [], "asks": [{"price": "0.42", "size": "10"}]}
            ),
            "missing_bid",
        )
        self.assertEqual(
            score_markets.spread_missing_reason(
                {"bids": [{"price": "0.40", "size": "10"}], "asks": []}
            ),
            "missing_ask",
        )

    def test_spread_missing_reason_preserves_fetch_failure(self):
        self.assertEqual(
            score_markets.spread_missing_reason(
                None, fetch_status="request_failed"
            ),
            "orderbook_request_failed",
        )

    def test_existing_snapshot_key_shape_matches_append_guard(self):
        row = {"market_id": 1, "score_version": "v0.2", "observed_at": "2026-06-13T00:00:00Z"}
        key = (str(row["market_id"]), row["score_version"], row["observed_at"])
        self.assertEqual(key, ("1", "v0.2", "2026-06-13T00:00:00Z"))


class FetchFilterTests(unittest.TestCase):
    def test_usable_rejects_already_expired_market(self):
        self.assertFalse(
            fetch_polymarket_markets.usable(
                {"clobTokenIds": '["a", "b"]', "endDate": "2020-01-01T00:00:00Z"}
            )
        )

    def test_usable_accepts_future_market(self):
        self.assertTrue(
            fetch_polymarket_markets.usable(
                {"clobTokenIds": '["a", "b"]', "endDate": "2099-01-01T00:00:00Z"}
            )
        )

    def test_collection_policy_and_bucket_targets(self):
        # widened, stratified breadth; a medium-horizon bucket exists
        self.assertEqual(fetch_polymarket_markets.COLLECTION_POLICY_VERSION, "v0.2-wide-300")
        targets = dict(fetch_polymarket_markets.BUCKET_TARGETS)
        self.assertIn("medium_horizon", targets)
        self.assertEqual(sum(targets.values()), 300)

    def test_slim_metadata_and_rank_shape(self):
        slim = fetch_polymarket_markets.slim_metadata(
            {"id": 7, "question": "Q?", "endDate": "2099-01-01T00:00:00Z",
             "volumeNum": 1000, "outcomes": '["Yes", "No"]'}
        )
        self.assertEqual(slim["market_id"], "7")
        self.assertEqual(slim["volume_usd"], 1000.0)
        self.assertEqual(slim["outcome_labels"], ["Yes", "No"])


class FreshnessTests(unittest.TestCase):
    def write_snapshot(self, directory, name, fetched_at):
        path = os.path.join(directory, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"fetched_at": fetched_at}, f)
        return path

    def test_freshness_uses_embedded_fetch_time(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            self.write_snapshot(
                raw_dir,
                "raw_snapshot_20260613T000000Z.json",
                "2026-06-13T00:00:00Z",
            )
            status = check_data_freshness.freshness_status(
                raw_dir,
                max_age_hours=36,
                now=datetime(2026, 6, 14, 0, 0, tzinfo=timezone.utc),
            )
            self.assertTrue(status["ok"])
            self.assertEqual(status["age_hours"], 24.0)

    def test_freshness_flags_stale_or_missing_data(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            missing = check_data_freshness.freshness_status(
                raw_dir,
                now=datetime(2026, 6, 14, 13, 0, tzinfo=timezone.utc),
            )
            self.assertFalse(missing["ok"])
            self.assertEqual(missing["reason"], "no_valid_snapshot")

            self.write_snapshot(
                raw_dir,
                "raw_snapshot_20260613T000000Z.json",
                "2026-06-13T00:00:00Z",
            )
            stale = check_data_freshness.freshness_status(
                raw_dir,
                max_age_hours=36,
                now=datetime(2026, 6, 14, 13, 0, tzinfo=timezone.utc),
            )
            self.assertFalse(stale["ok"])
            self.assertEqual(stale["reason"], "snapshot_stale")
            self.assertEqual(stale["age_hours"], 37.0)


class ResolutionTests(unittest.TestCase):
    def test_extract_resolution_accepts_tiny_price_rounding(self):
        record = resolution_tracker.extract_resolution(
            {
                "id": "1",
                "closed": True,
                "conditionId": "condition",
                "question": "Up or down?",
                "outcomes": '["Up", "Down"]',
                "outcomePrices": '["0.9999999", "0.0000001"]',
                "closedTime": "2026-06-13T01:00:00Z",
            }
        )
        self.assertEqual(record["outcome_primary"], 1.0)
        self.assertEqual(record["winning_outcome_label"], "Up")

    def test_extract_resolution_rejects_uncollapsed_prices(self):
        record = resolution_tracker.extract_resolution(
            {
                "id": "1",
                "closed": True,
                "outcomePrices": '["0.999", "0.001"]',
                "closedTime": "2026-06-13T01:00:00Z",
            }
        )
        self.assertIsNone(record)


class ValidationReportTests(unittest.TestCase):
    def setUp(self):
        # Markets a and b close >=24h after their snapshots (primary-eligible);
        # market c only has a same-day snapshot (short-horizon descriptive).
        self.rows = [
            {
                "market_id": "a",
                "observed_at": "2026-06-12T10:00:00Z",
                "closed_time": "2026-06-14T12:00:00Z",
                "composite_trust_score": 20,
                "brier": 0.36,
                "validation_eligible": True,
                "spread_is_missing": False,
                "horizon_bucket": "0-7d",
                "category": "Sports",
                "market_type": "sports_prop",
                "score_version": "v0.2",
            },
            {
                "market_id": "a",
                "observed_at": "2026-06-12T11:00:00Z",
                "closed_time": "2026-06-14T12:00:00Z",
                "composite_trust_score": 30,
                "brier": 0.36,
                "validation_eligible": True,
                "spread_is_missing": False,
                "horizon_bucket": "0-7d",
                "category": "Sports",
                "market_type": "sports_prop",
                "score_version": "v0.2",
            },
            {
                "market_id": "b",
                "observed_at": "2026-06-12T11:00:00Z",
                "closed_time": "2026-06-14T12:00:00Z",
                "composite_trust_score": 80,
                "brier": 0.01,
                "validation_eligible": True,
                "spread_is_missing": True,
                "horizon_bucket": "8-30d",
                "category": "Crypto",
                "market_type": "crypto_price",
                "score_version": "v0.2",
            },
            {
                "market_id": "c",
                "observed_at": "2026-06-12T23:00:00Z",
                "closed_time": "2026-06-13T01:00:00Z",
                "composite_trust_score": 40,
                "brier": 0.25,
                "validation_eligible": True,
                "spread_is_missing": False,
                "horizon_bucket": "0-7d",
                "category": "Sports",
                "market_type": "sports_prop",
                "score_version": "v0.2",
            },
        ]

    def test_report_uses_latest_24h_prior_snapshot_per_market(self):
        report = validation_report.build_report(self.rows)
        self.assertEqual(report["n_brier_rows"], 4)
        self.assertEqual(report["n_unique_resolved_markets"], 3)
        self.assertEqual(report["n_analysis_rows"], 2)
        self.assertEqual(report["primary_snapshot_rule"],
                         "latest eligible snapshot at least 24h before close")
        self.assertAlmostEqual(report["mean_brier"], 0.185)
        self.assertAlmostEqual(report["trust_vs_brier"]["correlation"], -1.0)
        self.assertEqual(report["trust_vs_brier_excluding_missing_spread"]["n"], 1)

    def test_same_day_market_goes_to_short_horizon_descriptive_not_primary(self):
        report = validation_report.build_report(self.rows)
        self.assertEqual(report["n_markets_excluded_no_24h_snapshot"], 1)
        self.assertEqual(report["short_horizon_descriptive"]["n"], 1)
        self.assertAlmostEqual(report["short_horizon_descriptive"]["mean_brier"], 0.25)
        # the same-day market must not leak into the primary trust buckets
        primary_n = sum(item["n"] for item in report["trust_buckets"])
        self.assertEqual(primary_n, 2)

    def test_snapshot_inside_24h_window_is_not_primary(self):
        primary = validation_report.primary_rows_24h_buffer(self.rows)
        self.assertEqual({row["market_id"] for row in primary}, {"a", "b"})
        # market a: the 11:00 snapshot is still >=24h before close, so it wins
        row_a = next(row for row in primary if row["market_id"] == "a")
        self.assertEqual(row_a["observed_at"], "2026-06-12T11:00:00Z")

    def test_svg_contains_points_and_fit(self):
        primary = validation_report.primary_rows_24h_buffer(self.rows)
        svg = validation_report.render_svg(primary)
        self.assertIn("<svg", svg)
        self.assertEqual(svg.count("<circle"), 2)
        self.assertIn('stroke="#dc2626"', svg)


if __name__ == "__main__":
    unittest.main()
