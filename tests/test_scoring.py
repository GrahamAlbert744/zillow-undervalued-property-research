"""
Tests for src/scoring.py, the Decision 019 MVP research-ranking score.

Covers the doc's core rules (docs/scoring_methodology.md):
- Missing data reduces the achievable score; it never inflates it
  (Decision 005).
- The total score never exceeds the documented max-achievable ceiling.
- Component scores stay within their documented point ranges.
- scripts/create_property_scores_table.py only scores properties already
  past candidate gating (Decision 013).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPTS_DIR))

from src.scoring import (  # noqa: E402
    MAX_ACHIEVABLE_SCORE,
    score_data_quality,
    score_income_potential,
    score_property,
    score_property_usefulness,
    score_valuation,
)

import create_property_scores_table as scores_stage  # noqa: E402


COMPLETE_ROW = {
    "basic_price_context_available": True,
    "price_per_sqft_vs_home_type_median_pct": -0.20,
    "zestimate_context_available": True,
    "price_to_zestimate_pct": -0.10,
    "rent_zestimate_available": True,
    "income_context_available": True,
    "gross_rent_yield": 0.08,
    "square_feet": 1500,
    "beds": 3,
    "baths": 2,
    "home_type": "single_family",
    "price": 500000,
    "address": "1 Test St",
    "latitude": 42.28,
    "longitude": -71.12,
    "outside_target_radius": False,
    "data_needs_review": False,
}

EMPTY_ROW: dict = {}


def test_total_score_never_exceeds_max_achievable() -> None:
    result = score_property(COMPLETE_ROW)
    assert result["total_research_score"] <= MAX_ACHIEVABLE_SCORE
    assert result["max_achievable_research_score"] == MAX_ACHIEVABLE_SCORE


def test_fully_favorable_row_reaches_max_achievable_score() -> None:
    result = score_property(COMPLETE_ROW)
    assert result["total_research_score"] == MAX_ACHIEVABLE_SCORE


def test_empty_row_scores_near_zero_not_something_higher() -> None:
    """
    Missing data must reduce the score, never inflate it (Decision 005).

    A completely empty row earns 0 on every component that requires a
    present value (valuation, income, usefulness, and the core-fields/
    geocode parts of data quality). The only nonzero credit it can get is
    the "no duplicate/suspicious warning" and "in target radius" data
    quality points, because those booleans follow the same
    missing-means-not-flagged convention already used upstream (see
    ensure_boolean() in create_valuation_context_features.py and
    is_outside_radius() in src/geocoding.py) rather than a value this
    module invents on its own.
    """
    result = score_property(EMPTY_ROW)
    assert result["valuation_score"] == 0
    assert result["income_potential_score"] == 0
    assert result["property_usefulness_score"] == 0
    assert result["data_quality_score"] <= 7  # only the two boolean-default points
    assert result["total_research_score"] <= 7


def test_missing_zestimate_context_does_not_penalize_below_zero() -> None:
    row = dict(COMPLETE_ROW)
    row["zestimate_context_available"] = False
    row["price_to_zestimate_pct"] = None
    points, notes = score_valuation(row)
    assert points >= 0
    assert any("Zestimate unavailable" in note for note in notes)


def test_valuation_score_within_documented_range() -> None:
    points, _ = score_valuation(COMPLETE_ROW)
    assert 0 <= points <= 40


def test_income_score_within_documented_range() -> None:
    points, _ = score_income_potential(COMPLETE_ROW)
    assert 0 <= points <= 25


def test_usefulness_score_within_documented_range() -> None:
    points, _ = score_property_usefulness(COMPLETE_ROW)
    assert 0 <= points <= 20


def test_data_quality_score_within_documented_range() -> None:
    points, _ = score_data_quality(COMPLETE_ROW)
    assert 0 <= points <= 15


def test_non_residential_home_type_gets_no_usefulness_credit_for_type() -> None:
    row = dict(COMPLETE_ROW)
    row["home_type"] = "land"
    points, notes = score_property_usefulness(row)
    assert points < 20
    assert any("residential type" in note for note in notes)


def test_outside_radius_loses_data_quality_credit() -> None:
    row = dict(COMPLETE_ROW)
    row["outside_target_radius"] = True
    points, notes = score_data_quality(row)
    assert points < 15
    assert any("outside the target radius" in note for note in notes)


def test_data_needs_review_flag_loses_credit() -> None:
    row = dict(COMPLETE_ROW)
    row["data_needs_review"] = True
    points, notes = score_data_quality(row)
    assert points < 15
    assert any("flagged for data-quality review" in note for note in notes)


def test_reject_and_hold_buckets_are_not_scored(monkeypatch, tmp_path) -> None:
    """Decision 013: candidate gating happens before scoring, not after."""
    df = pd.DataFrame(
        [
            {**COMPLETE_ROW, "candidate_review_bucket": "reject", "property_id": "r1"},
            {**COMPLETE_ROW, "candidate_review_bucket": "hold", "property_id": "h1"},
            {**COMPLETE_ROW, "candidate_review_bucket": "rankable_later", "property_id": "ok1"},
            {**COMPLETE_ROW, "candidate_review_bucket": "needs_review", "property_id": "nr1"},
        ]
    )

    input_path = tmp_path / "valuation_context_features.csv"
    df.to_csv(input_path, index=False)

    monkeypatch.setattr(scores_stage, "INPUT_PATH", input_path)

    result_df = scores_stage.create_property_scores()
    by_id = result_df.set_index("property_id")

    assert bool(by_id.loc["r1", "research_score_created"]) is False
    assert bool(by_id.loc["h1", "research_score_created"]) is False
    assert bool(by_id.loc["ok1", "research_score_created"]) is True
    assert bool(by_id.loc["nr1", "research_score_created"]) is True

    assert pd.isna(by_id.loc["r1", "total_research_score"])
    assert pd.isna(by_id.loc["h1", "total_research_score"])
    assert by_id.loc["ok1", "total_research_score"] > 0


def test_scores_table_never_sets_forbidden_anti_overclaim_flags(monkeypatch, tmp_path) -> None:
    df = pd.DataFrame([{**COMPLETE_ROW, "candidate_review_bucket": "rankable_later", "property_id": "ok1"}])
    input_path = tmp_path / "valuation_context_features.csv"
    df.to_csv(input_path, index=False)

    monkeypatch.setattr(scores_stage, "INPUT_PATH", input_path)

    result_df = scores_stage.create_property_scores()

    assert not result_df["fair_value_estimate_created"].any()
    assert not result_df["investment_recommendation_created"].any()
    assert not result_df["buy_sell_recommendation_created"].any()
    assert not result_df["backtesting_ready"].any()
