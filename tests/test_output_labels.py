"""
Tests for src/output_labels.py (Decision 020).

Covers CLAUDE.md's guardrail: "Allowed output labels are limited to:
research first, watchlist, avoid, possible candidate after human review,
needs data review." This is the positive-allowlist counterpart to
tests/test_research_notes_language.py's forbidden-language checks.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPTS_DIR))

import pytest  # noqa: E402

from src.output_labels import (  # noqa: E402
    ALLOWED_OUTPUT_LABELS,
    EXCLUSION_TYPE_TO_LABEL,
    QUEUE_BUCKET_TO_LABEL,
    assert_valid_label,
    label_for_exclusion_type,
    label_for_queue_bucket,
)


def test_every_queue_bucket_maps_to_an_allowed_label() -> None:
    for bucket, label in QUEUE_BUCKET_TO_LABEL.items():
        assert label in ALLOWED_OUTPUT_LABELS, f"{bucket} -> {label!r} is not allowed"


def test_every_exclusion_type_maps_to_an_allowed_label() -> None:
    for exclusion_type, label in EXCLUSION_TYPE_TO_LABEL.items():
        assert label in ALLOWED_OUTPUT_LABELS, f"{exclusion_type} -> {label!r} is not allowed"


def test_all_known_queue_buckets_are_covered() -> None:
    """
    Every bucket assign_research_queue_bucket() can produce (see
    scripts/create_research_queue_table.py) must have a mapping, or scoring
    a real pipeline run would raise.
    """
    known_buckets = {
        "review_first",
        "review_next",
        "review_if_time",
        "watchlist_limited_data",
        "data_quality_review",
        "excluded",
    }
    assert known_buckets == set(QUEUE_BUCKET_TO_LABEL.keys())


def test_all_known_exclusion_types_are_covered() -> None:
    known_exclusion_types = {"reject", "hold", "needs_review"}
    assert known_exclusion_types == set(EXCLUSION_TYPE_TO_LABEL.keys())


def test_assert_valid_label_accepts_allowed_labels() -> None:
    for label in ALLOWED_OUTPUT_LABELS:
        assert assert_valid_label(label) == label


def test_assert_valid_label_rejects_forbidden_label() -> None:
    with pytest.raises(ValueError):
        assert_valid_label("strong buy")


def test_label_for_queue_bucket_raises_on_unknown_bucket() -> None:
    with pytest.raises(ValueError):
        label_for_queue_bucket("some_new_bucket_nobody_mapped_yet")


def test_label_for_exclusion_type_raises_on_unknown_type() -> None:
    with pytest.raises(ValueError):
        label_for_exclusion_type("some_new_type_nobody_mapped_yet")


def test_research_queue_rows_all_have_an_allowed_label(monkeypatch, tmp_path) -> None:
    """End-to-end: create_research_queue() must attach a valid label to every row."""
    import create_research_queue_table as queue_stage

    row_template = {
        "property_id": "p1",
        "candidate_review_bucket": "rankable_later",
        "data_needs_review": False,
        "basic_price_context_available": True,
        "valuation_context_signal_count": 3,
        "below_home_type_median_ppsf": True,
        "far_below_home_type_median_ppsf": True,
        "listing_price_below_zestimate_context": False,
        "moderate_gross_rent_yield_context": False,
        "high_gross_rent_yield_context": False,
        "zestimate_available": False,
        "rent_zestimate_available": False,
        "price_per_sqft_vs_home_type_median_pct": -0.2,
    }

    df = pd.DataFrame([row_template])
    input_path = tmp_path / "property_scores.csv"
    df.to_csv(input_path, index=False)

    monkeypatch.setattr(queue_stage, "INPUT_PATH", input_path)

    result_df = queue_stage.create_research_queue()

    assert (result_df["conservative_output_label"].isin(ALLOWED_OUTPUT_LABELS)).all()


def test_exclusion_review_rows_all_have_an_allowed_label(monkeypatch, tmp_path) -> None:
    """End-to-end: create_exclusion_review_table() must attach a valid label to every row."""
    import create_candidate_exclusion_review_table as exclusion_stage

    df = pd.DataFrame(
        [
            {"property_id": "r1", "candidate_review_bucket": "reject", "address": "1 A St"},
            {"property_id": "h1", "candidate_review_bucket": "hold", "address": "2 B St"},
            {"property_id": "n1", "candidate_review_bucket": "needs_review", "address": "3 C St"},
        ]
    )

    input_path = tmp_path / "active_listing_candidate_table.csv"
    df.to_csv(input_path, index=False)

    monkeypatch.setattr(exclusion_stage, "CANDIDATE_INPUT_PATH", input_path)
    monkeypatch.setattr(exclusion_stage, "QUEUE_INPUT_PATH", tmp_path / "does_not_exist.csv")

    result_df = exclusion_stage.create_exclusion_review_table()

    assert (result_df["conservative_output_label"].isin(ALLOWED_OUTPUT_LABELS)).all()
