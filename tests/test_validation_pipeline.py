import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import fetch_polymarket_markets
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
        self.rows = [
            {
                "market_id": "a",
                "observed_at": "2026-06-12T10:00:00Z",
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
                "composite_trust_score": 80,
                "brier": 0.01,
                "validation_eligible": True,
                "spread_is_missing": True,
                "horizon_bucket": "8-30d",
                "category": "Crypto",
                "market_type": "crypto_price",
                "score_version": "v0.2",
            },
        ]

    def test_report_uses_latest_snapshot_per_market(self):
        report = validation_report.build_report(self.rows)
        self.assertEqual(report["n_brier_rows"], 3)
        self.assertEqual(report["n_unique_resolved_markets"], 2)
        self.assertEqual(report["n_analysis_rows"], 2)
        self.assertAlmostEqual(report["mean_brier"], 0.185)
        self.assertAlmostEqual(report["trust_vs_brier"]["correlation"], -1.0)
        self.assertEqual(report["trust_vs_brier_excluding_missing_spread"]["n"], 1)

    def test_svg_contains_points_and_fit(self):
        primary = validation_report.latest_rows(self.rows)
        svg = validation_report.render_svg(primary)
        self.assertIn("<svg", svg)
        self.assertEqual(svg.count("<circle"), 2)
        self.assertIn('stroke="#dc2626"', svg)


if __name__ == "__main__":
    unittest.main()
