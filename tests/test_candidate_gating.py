"""
Tests for the conservative candidate-gating logic in
scripts/create_active_listing_candidate_table.py.

Per Decision 013 in docs/decision_log.md, candidate gating must happen
before any scoring, and it must sort properties into reject / hold /
needs_review / rankable_later states based on hard data-quality gates only.
These tests pin that ordering and bucket mapping.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import create_active_listing_candidate_table as candidate  # noqa: E402


BASE_ROW = {
    "outside_target_radius": False,
    "is_residential_property": True,
    "undisclosed_address": False,
    "missing_price": False,
    "missing_square_feet": False,
    "missing_beds": False,
    "missing_baths": False,
    "missing_lat_long": False,
    "missing_home_type": False,
    "data_needs_review": False,
}


def make_row(**overrides: object) -> pd.Series:
    data = dict(BASE_ROW)
    data.update(overrides)
    # dtype=object preserves plain Python bool identity (True/False), which
    # create_candidate_state() relies on via `is True` checks. A default
    # pd.Series(data) would upcast these to numpy.bool_, silently breaking
    # those identity checks.
    return pd.Series(data, dtype=object)


@pytest.mark.parametrize(
    "overrides, expected_state, expected_bucket",
    [
        ({}, "rankable_after_scoring_phase", "rankable_later"),
        ({"outside_target_radius": True}, "reject_outside_radius", "reject"),
        ({"is_residential_property": False}, "reject_non_residential", "reject"),
        ({"missing_price": True}, "reject_missing_price", "reject"),
        ({"undisclosed_address": True}, "needs_manual_review", "needs_review"),
        ({"missing_square_feet": True}, "hold_missing_square_feet", "hold"),
        ({"missing_beds": True}, "hold_missing_core_property_details", "hold"),
        ({"missing_baths": True}, "hold_missing_core_property_details", "hold"),
        ({"missing_lat_long": True}, "hold_missing_geography", "hold"),
        ({"missing_home_type": True}, "hold_missing_home_type", "hold"),
        ({"data_needs_review": True}, "needs_data_review", "needs_review"),
    ],
)
def test_candidate_state_and_bucket(overrides, expected_state, expected_bucket) -> None:
    row = make_row(**overrides)
    state = candidate.create_candidate_state(row)
    assert state == expected_state

    row_with_state = row.copy()
    row_with_state["candidate_state"] = state
    bucket = candidate.create_candidate_review_bucket(row_with_state)
    assert bucket == expected_bucket


def test_outside_radius_is_checked_before_missing_price() -> None:
    """Gate ordering matters: reject_outside_radius must win over other issues."""
    row = make_row(outside_target_radius=True, missing_price=True)
    assert candidate.create_candidate_state(row) == "reject_outside_radius"


def test_undisclosed_address_is_checked_before_missing_square_feet() -> None:
    """needs_manual_review must win over hold-tier issues per the gate order."""
    row = make_row(undisclosed_address=True, missing_square_feet=True)
    assert candidate.create_candidate_state(row) == "needs_manual_review"


def test_clean_row_is_rankable_later_not_scored() -> None:
    """A fully clean row is gated as rankable_later, never scored directly."""
    row = make_row()
    state = candidate.create_candidate_state(row)
    row_with_state = row.copy()
    row_with_state["candidate_state"] = state
    bucket = candidate.create_candidate_review_bucket(row_with_state)

    assert state == "rankable_after_scoring_phase"
    assert bucket == "rankable_later"
