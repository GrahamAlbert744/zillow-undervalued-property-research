"""
Conservative MVP research-ranking score (Decision 019).

Purpose:
- Implement the 100-point framework already specced in
  docs/scoring_methodology.md: Valuation (40) / Income Potential (25) /
  Property Usefulness (20) / Data Quality (15).
- Use only the signals the methodology doc marks as ready now. Signals it
  explicitly defers as "future feature" (comparable-sale discount, HOA/tax
  burden, multifamily-use potential, price-cut/days-on-market history,
  useful-size/layout refinement) are left at 0 and documented as
  unavailable rather than guessed.
- Missing data reduces the achievable score; it must never inflate it
  (Decision 005).

This module does not decide buy/sell/hold. It does not estimate fair value.
It produces a transparent, explainable ranking signal for human research
triage only, consumed by scripts/create_property_scores_table.py.

Because several of the doc's planned signals are not yet available from the
current pipeline (no days-on-market/price-history, no HOA data, no comp
engine), the maximum score actually achievable in this MVP version is 82,
not 100. This is intentional — see docs/scoring_methodology.md and
docs/decision_log.md Decision 019 for the full breakdown of which planned
signals are implemented vs. deferred.
"""

from __future__ import annotations

from typing import Any

RESIDENTIAL_HOME_TYPES = {"single_family", "condo", "townhome", "multi_family"}

# Valuation (40 points total; only 30 achievable in this MVP version)
VALUATION_PPSF_MAX_POINTS = 20
VALUATION_ZESTIMATE_MAX_POINTS = 10
VALUATION_PPSF_FULL_CREDIT_DISCOUNT = -0.20  # 20% below home-type median ppsf
VALUATION_ZESTIMATE_FULL_CREDIT_DISCOUNT = -0.10  # 10% below Zestimate

# Income potential (25 points total; only 17 achievable in this MVP version)
INCOME_RENT_ZESTIMATE_AVAILABLE_POINTS = 5
INCOME_GROSS_YIELD_MAX_POINTS = 12
# Matches the thresholds already used by
# scripts/create_valuation_context_features.py, so scoring and context
# flags stay consistent with each other.
GROSS_YIELD_HIGH_THRESHOLD = 0.055
GROSS_YIELD_MODERATE_THRESHOLD = 0.045
GROSS_YIELD_TOP_THRESHOLD = 0.07

# Property usefulness (20 points total; all 20 achievable)
USEFULNESS_SQFT_POINTS = 5
USEFULNESS_BEDS_BATHS_POINTS = 5
USEFULNESS_RESIDENTIAL_TYPE_POINTS = 5
USEFULNESS_VALID_PRICE_POINTS = 5

# Data quality (15 points total; all 15 achievable)
DATA_QUALITY_CORE_FIELDS_POINTS = 5
DATA_QUALITY_GEOCODE_POINTS = 3
DATA_QUALITY_IN_RADIUS_POINTS = 3
DATA_QUALITY_NO_REVIEW_FLAG_POINTS = 4

MAX_ACHIEVABLE_SCORE = (
    VALUATION_PPSF_MAX_POINTS
    + VALUATION_ZESTIMATE_MAX_POINTS
    + INCOME_RENT_ZESTIMATE_AVAILABLE_POINTS
    + INCOME_GROSS_YIELD_MAX_POINTS
    + USEFULNESS_SQFT_POINTS
    + USEFULNESS_BEDS_BATHS_POINTS
    + USEFULNESS_RESIDENTIAL_TYPE_POINTS
    + USEFULNESS_VALID_PRICE_POINTS
    + DATA_QUALITY_CORE_FIELDS_POINTS
    + DATA_QUALITY_GEOCODE_POINTS
    + DATA_QUALITY_IN_RADIUS_POINTS
    + DATA_QUALITY_NO_REVIEW_FLAG_POINTS
)


def _is_true(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    try:
        if value != value:  # NaN check without importing pandas here
            return False
    except TypeError:
        pass
    return bool(value)


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    try:
        if value != value:  # NaN
            return False
    except TypeError:
        pass
    return True


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _linear_credit(
    discount_pct: float | None,
    full_credit_discount: float,
    max_points: float,
) -> float:
    """
    Scale points linearly from 0 (at 0% discount) to max_points (at
    full_credit_discount or beyond). discount_pct is expected negative for
    a discount (e.g. -0.10 = 10% cheaper). Positive (premium) values score 0.
    """
    if discount_pct is None:
        return 0.0

    if discount_pct >= 0:
        return 0.0

    fraction = discount_pct / full_credit_discount  # both negative -> positive fraction
    fraction = _clamp(fraction, 0.0, 1.0)

    return round(fraction * max_points, 2)


def score_valuation(row: dict[str, Any]) -> tuple[float, list[str]]:
    """Valuation score (0-40, 30 achievable in this MVP version)."""
    notes: list[str] = []
    points = 0.0

    if _is_true(row.get("basic_price_context_available")):
        ppsf_points = _linear_credit(
            row.get("price_per_sqft_vs_home_type_median_pct"),
            VALUATION_PPSF_FULL_CREDIT_DISCOUNT,
            VALUATION_PPSF_MAX_POINTS,
        )
        points += ppsf_points
        if ppsf_points == 0:
            notes.append("Price per sqft is not below the home-type median.")
    else:
        notes.append("Price-per-sqft benchmark context unavailable; valuation ppsf credit withheld.")

    if _is_true(row.get("zestimate_context_available")):
        zestimate_points = _linear_credit(
            row.get("price_to_zestimate_pct"),
            VALUATION_ZESTIMATE_FULL_CREDIT_DISCOUNT,
            VALUATION_ZESTIMATE_MAX_POINTS,
        )
        points += zestimate_points
        if zestimate_points == 0:
            notes.append("Listing price is not below Zestimate.")
    else:
        notes.append("Zestimate unavailable; valuation Zestimate credit withheld.")

    notes.append(
        "Price-cut/days-on-market and comparable-sale-discount signals are "
        "not yet available (10 of 40 valuation points not implemented)."
    )

    return round(points, 2), notes


def score_income_potential(row: dict[str, Any]) -> tuple[float, list[str]]:
    """Income potential score (0-25, 17 achievable in this MVP version)."""
    notes: list[str] = []
    points = 0.0

    if _is_true(row.get("rent_zestimate_available")):
        points += INCOME_RENT_ZESTIMATE_AVAILABLE_POINTS
    else:
        notes.append("Rent Zestimate unavailable.")

    gross_rent_yield = row.get("gross_rent_yield")

    if _is_true(row.get("income_context_available")) and _has_value(gross_rent_yield):
        yield_value = float(gross_rent_yield)
        if yield_value >= GROSS_YIELD_TOP_THRESHOLD:
            yield_points = INCOME_GROSS_YIELD_MAX_POINTS
        elif yield_value >= GROSS_YIELD_HIGH_THRESHOLD:
            yield_points = 9
        elif yield_value >= GROSS_YIELD_MODERATE_THRESHOLD:
            yield_points = 6
        elif yield_value > 0:
            yield_points = 3
        else:
            yield_points = 0
        points += yield_points
    else:
        notes.append("Gross rent yield context unavailable.")

    notes.append(
        "HOA/tax burden and multifamily rental-use potential are not yet "
        "implemented (8 of 25 income points not implemented)."
    )

    return round(points, 2), notes


def score_property_usefulness(row: dict[str, Any]) -> tuple[float, list[str]]:
    """Property usefulness score (0-20, all 20 achievable)."""
    notes: list[str] = []
    points = 0.0

    square_feet = row.get("square_feet")
    if _has_value(square_feet) and float(square_feet) > 0:
        points += USEFULNESS_SQFT_POINTS
    else:
        notes.append("Missing or invalid square footage.")

    beds = row.get("beds")
    baths = row.get("baths")
    if _has_value(beds) and _has_value(baths):
        points += USEFULNESS_BEDS_BATHS_POINTS
    else:
        notes.append("Missing beds and/or baths.")

    home_type = row.get("home_type")
    if home_type in RESIDENTIAL_HOME_TYPES:
        points += USEFULNESS_RESIDENTIAL_TYPE_POINTS
    else:
        notes.append("Home type missing or not a recognized residential type.")

    price = row.get("price")
    if _has_value(price) and float(price) > 0:
        points += USEFULNESS_VALID_PRICE_POINTS
    else:
        notes.append("Missing or invalid listing price.")

    return round(points, 2), notes


def score_data_quality(row: dict[str, Any]) -> tuple[float, list[str]]:
    """Data quality score (0-15, all 15 achievable)."""
    notes: list[str] = []
    points = 0.0

    core_fields = ["price", "square_feet", "beds", "baths", "home_type", "address"]
    core_complete = all(_has_value(row.get(field)) for field in core_fields)
    if core_complete:
        points += DATA_QUALITY_CORE_FIELDS_POINTS
    else:
        notes.append("One or more core fields (price, sqft, beds, baths, type, address) missing.")

    latitude = row.get("latitude")
    longitude = row.get("longitude")
    if _has_value(latitude) and _has_value(longitude):
        points += DATA_QUALITY_GEOCODE_POINTS
    else:
        notes.append("Missing latitude/longitude.")

    if not _is_true(row.get("outside_target_radius")):
        points += DATA_QUALITY_IN_RADIUS_POINTS
    else:
        notes.append("Property is outside the target radius.")

    # The pipeline currently exposes one combined data-quality review flag
    # (data_needs_review) rather than separate duplicate/suspicious-value
    # flags, so both the "no duplicate warning" (2 pts) and "no suspicious
    # value warning" (2 pts) rows from docs/scoring_methodology.md are
    # scored together from that single flag.
    if not _is_true(row.get("data_needs_review")):
        points += DATA_QUALITY_NO_REVIEW_FLAG_POINTS
    else:
        notes.append("Record is flagged for data-quality review.")

    return round(points, 2), notes


def score_property(row: dict[str, Any]) -> dict[str, Any]:
    """
    Score a single property row (as a dict of column -> value).

    Returns component scores, total score, and a combined confidence-notes
    string. Does not decide eligibility — callers should only score rows
    already past candidate gating (candidate_review_bucket not in
    {reject, hold}), per Decision 013.
    """
    valuation_points, valuation_notes = score_valuation(row)
    income_points, income_notes = score_income_potential(row)
    usefulness_points, usefulness_notes = score_property_usefulness(row)
    data_quality_points, data_quality_notes = score_data_quality(row)

    total = round(
        valuation_points + income_points + usefulness_points + data_quality_points,
        2,
    )

    all_notes = valuation_notes + income_notes + usefulness_notes + data_quality_notes

    return {
        "valuation_score": valuation_points,
        "income_potential_score": income_points,
        "property_usefulness_score": usefulness_points,
        "data_quality_score": data_quality_points,
        "total_research_score": total,
        "max_achievable_research_score": MAX_ACHIEVABLE_SCORE,
        "score_confidence_notes": " ".join(all_notes),
    }
