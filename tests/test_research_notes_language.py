"""
Tests for the forbidden buy/sell/investment-language check in
scripts/create_property_research_notes.py.

This check is the mechanical enforcement behind the project's core
guardrail (see CLAUDE.md and docs/decision_log.md Decision 003/015): notes
must never contain buy/sell/investment-recommendation language, even inside
a disclaimer sentence.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import create_property_research_notes as notes  # noqa: E402


def test_clean_text_has_no_forbidden_matches() -> None:
    text = (
        "This note is generated for human research triage only. It is not "
        "a purchase or sale recommendation and does not represent a "
        "completed valuation."
    )
    assert notes.check_forbidden_language(text) == []


def test_detects_buy_as_whole_word() -> None:
    assert notes.check_forbidden_language("Consider whether to buy this property.")


def test_does_not_false_positive_on_buy_as_substring() -> None:
    # "buyer" contains "buy" but the pattern is word-bounded, so it must not match.
    text = "The buyer's agent should confirm listing details."
    assert notes.check_forbidden_language(text) == []


def test_detects_sell_as_whole_word() -> None:
    assert notes.check_forbidden_language("This might be a good time to sell.")


def test_detects_strong_buy_phrase() -> None:
    assert notes.check_forbidden_language("This is a strong buy candidate.")


def test_detects_guaranteed_undervalued_phrase() -> None:
    assert notes.check_forbidden_language(
        "This property is a guaranteed undervalued opportunity."
    )


def test_detects_safe_investment_phrase() -> None:
    assert notes.check_forbidden_language("This is a safe investment.")


def test_detects_confirmed_bargain_phrase() -> None:
    assert notes.check_forbidden_language("This is a confirmed bargain.")


def test_detects_final_valuation_phrase() -> None:
    assert notes.check_forbidden_language("Here is the final valuation for this home.")


def test_detection_is_case_insensitive() -> None:
    assert notes.check_forbidden_language("STRONG BUY signal detected.")


def test_negated_disclaimer_still_triggers_the_check() -> None:
    # This is the exact failure mode Decision 015 called out: a negated
    # disclaimer ("not a buy or sell recommendation") still contains the
    # literal forbidden words and must still be caught.
    text = "This is not a buy or sell recommendation."
    matches = notes.check_forbidden_language(text)
    assert matches, "negated disclaimer sentence must still be flagged"


def test_build_note_raises_before_writing_forbidden_language(monkeypatch, tmp_path) -> None:
    """create_notes() must raise, not write, when a note contains forbidden language."""
    import pandas as pd

    bad_row = {
        "property_id": "test-001",
        "address": "1 Test St",
        "home_type": "single_family",
        "status_text": "For sale",
        "home_status": "FOR_SALE",
        "price": 500000,
        "beds": 3,
        "baths": 2,
        "square_feet": 1500,
        "lot_size": None,
        "lot_size_units": None,
        "price_per_sqft": 333.0,
        "distance_from_02131_miles": 5.0,
        "zillow_url": "https://example.com",
        "search_date": "2026-01-01",
        "data_source": "zillow_connector",
        "research_queue_position": 1,
        "research_queue_bucket": "review_first",
        "conservative_output_label": "research first",
        "research_priority": "high",
        "search_level_record_only": True,
        "zestimate": None,
        "zestimate_available": False,
        "rent_zestimate": None,
        "rent_zestimate_available": False,
        "detail_pull_completed": False,
        "price_per_sqft_vs_home_type_median_pct": None,
        "below_home_type_median_ppsf": False,
        "far_below_home_type_median_ppsf": False,
        "valuation_context_signal_count": 0,
        "valuation_context_bucket": "low_context",
        "context_confidence_notes": "strong buy signal",  # forbidden phrase injected
        "candidate_state": "rankable_after_scoring_phase",
        "candidate_review_bucket": "rankable_later",
        "data_needs_review": False,
        "outside_target_radius": False,
        "next_research_steps": "Confirm listing details.",
        "research_queue_not_investment_ranking": True,
        "final_score_created": False,
        "investment_recommendation_created": False,
        "buy_sell_recommendation_created": False,
        "backtesting_ready": False,
    }

    queue_df = pd.DataFrame([bad_row])
    input_path = tmp_path / "property_research_queue.csv"
    queue_df.to_csv(input_path, index=False)

    monkeypatch.setattr(notes, "INPUT_PATH", input_path)
    monkeypatch.setattr(notes, "NOTES_DIR", tmp_path / "notes")

    try:
        notes.create_notes()
        raised = False
    except ValueError:
        raised = True

    assert raised, "create_notes() must raise ValueError instead of writing a note with forbidden language"
    assert not (tmp_path / "notes").exists() or not any((tmp_path / "notes").iterdir())
