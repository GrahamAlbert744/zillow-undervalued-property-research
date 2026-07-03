"""
Create active-listing candidate table.

Purpose:
- Convert normalized active Zillow search-level records into a conservative
  candidate-review table.
- Apply hard data-quality gates before any scoring.
- Preserve review states: rankable, hold, needs_review, reject.
- Do NOT build valuation scoring yet.
- Do NOT recommend buying or selling.

Inputs:
- data/processed/all_properties_normalized.csv

Outputs:
- data/interim/active_listing_candidate_table.csv
- outputs/tables/active_listing_candidate_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.geocoding import is_outside_radius
except ModuleNotFoundError:
    from geocoding import is_outside_radius


INPUT_PATH = Path("data/processed/all_properties_normalized.csv")
OUTPUT_PATH = Path("data/interim/active_listing_candidate_table.csv")
SUMMARY_PATH = Path("outputs/tables/active_listing_candidate_summary.csv")


RESIDENTIAL_HOME_TYPES = {
    "single_family",
    "condo",
    "townhome",
    "multi_family",
}


def normalize_text(value: object) -> str | None:
    """Normalize string values."""
    if pd.isna(value):
        return None

    text = str(value).strip()

    if text == "":
        return None

    return text


def is_missing_series(series: pd.Series) -> pd.Series:
    """Return missing-value boolean series."""
    return series.isna() | series.astype(str).str.strip().eq("")


def create_candidate_state(row: pd.Series) -> str:
    """
    Assign conservative review state.

    This is gating, not scoring.
    """
    if row["outside_target_radius"] is True:
        return "reject_outside_radius"

    if row["is_residential_property"] is False:
        return "reject_non_residential"

    if row["undisclosed_address"] is True:
        return "needs_manual_review"

    if row["missing_price"] is True:
        return "reject_missing_price"

    if row["missing_square_feet"] is True:
        return "hold_missing_square_feet"

    if row["missing_beds"] is True or row["missing_baths"] is True:
        return "hold_missing_core_property_details"

    if row["missing_lat_long"] is True:
        return "hold_missing_geography"

    if row["missing_home_type"] is True:
        return "hold_missing_home_type"

    if row["data_needs_review"] is True:
        return "needs_data_review"

    return "rankable_after_scoring_phase"


def create_candidate_review_bucket(row: pd.Series) -> str:
    """
    Create simple top-level queue bucket.

    This is still not a score.
    """
    state = row["candidate_state"]

    if state.startswith("reject"):
        return "reject"

    if state.startswith("hold"):
        return "hold"

    if state == "needs_manual_review" or state == "needs_data_review":
        return "needs_review"

    if state == "rankable_after_scoring_phase":
        return "rankable_later"

    return "needs_review"


def create_active_listing_candidate_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create active-listing candidate table from normalized properties."""
    df = df.copy()

    required_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "home_status",
        "status_text",
        "home_type",
        "fixture_classification",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "zestimate",
        "rent_zestimate",
        "price_to_zestimate_pct",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "new_construction_available_plan_count",
        "new_construction_premier_builder",
        "has_open_house",
        "has_vr_model",
        "title",
        "zillow_url",
        "search_date",
        "data_source",
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["home_type"] = df["home_type"].apply(normalize_text)

    df["is_residential_property"] = df["home_type"].isin(RESIDENTIAL_HOME_TYPES)

    df["missing_price"] = df["price"].isna()
    df["missing_square_feet"] = df["square_feet"].isna()
    df["missing_beds"] = df["beds"].isna()
    df["missing_baths"] = df["baths"].isna()
    df["missing_home_type"] = is_missing_series(df["home_type"])
    df["missing_lat_long"] = df["latitude"].isna() | df["longitude"].isna()

    df["undisclosed_address"] = (
        df["address"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains("undisclosed")
    )

    df["invalid_price"] = df["price"].notna() & (df["price"] <= 0)
    df["invalid_square_feet"] = df["square_feet"].notna() & (df["square_feet"] <= 0)

    df["suspiciously_low_price_per_sqft"] = (
        df["price_per_sqft"].notna() & (df["price_per_sqft"] < 150)
    )

    df["suspiciously_high_price_per_sqft"] = (
        df["price_per_sqft"].notna() & (df["price_per_sqft"] > 1500)
    )

    if "outside_target_radius" not in df.columns:
        df["outside_target_radius"] = None

    df["outside_target_radius"] = df["outside_target_radius"].apply(
        lambda value: bool(value) if pd.notna(value) else None
    )

    df["zillow_active_listing_candidate"] = True

    df["search_level_record_only"] = True
    df["detail_pull_completed"] = False
    df["zestimate_needs_detail_validation"] = df["zestimate"].isna()
    df["rent_zestimate_needs_detail_validation"] = df["rent_zestimate"].isna()
    df["days_on_market_available"] = False
    df["price_history_available"] = False
    df["tax_history_available"] = False
    df["listing_description_available"] = False
    df["hoa_fee_available"] = False
    df["property_tax_available"] = False

    df["valuation_scoring_ready"] = False
    df["income_scoring_ready"] = False
    df["market_signal_scoring_ready"] = False
    df["text_signal_scoring_ready"] = False
    df["overall_scoring_ready"] = False

    df["data_needs_review"] = (
        df["missing_price"]
        | df["missing_square_feet"]
        | df["missing_beds"]
        | df["missing_baths"]
        | df["missing_home_type"]
        | df["missing_lat_long"]
        | df["undisclosed_address"]
        | df["invalid_price"]
        | df["invalid_square_feet"]
        | df["suspiciously_low_price_per_sqft"]
        | df["suspiciously_high_price_per_sqft"]
    )

    df["candidate_state"] = df.apply(create_candidate_state, axis=1)
    df["candidate_review_bucket"] = df.apply(create_candidate_review_bucket, axis=1)

    df["candidate_notes"] = (
        "Active listing search-level record only. Candidate state is based on "
        "hard data-quality gates, not valuation scoring."
    )

    output_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "home_status",
        "status_text",
        "home_type",
        "fixture_classification",
        "is_residential_property",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "zestimate",
        "rent_zestimate",
        "price_to_zestimate_pct",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "new_construction_available_plan_count",
        "new_construction_premier_builder",
        "has_open_house",
        "has_vr_model",
        "title",
        "zillow_active_listing_candidate",
        "search_level_record_only",
        "detail_pull_completed",
        "zestimate_needs_detail_validation",
        "rent_zestimate_needs_detail_validation",
        "days_on_market_available",
        "price_history_available",
        "tax_history_available",
        "listing_description_available",
        "hoa_fee_available",
        "property_tax_available",
        "missing_price",
        "missing_square_feet",
        "missing_beds",
        "missing_baths",
        "missing_home_type",
        "missing_lat_long",
        "undisclosed_address",
        "invalid_price",
        "invalid_square_feet",
        "suspiciously_low_price_per_sqft",
        "suspiciously_high_price_per_sqft",
        "data_needs_review",
        "valuation_scoring_ready",
        "income_scoring_ready",
        "market_signal_scoring_ready",
        "text_signal_scoring_ready",
        "overall_scoring_ready",
        "candidate_state",
        "candidate_review_bucket",
        "zillow_url",
        "search_date",
        "data_source",
        "candidate_notes",
    ]

    return df[output_columns]


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create candidate table summary."""
    rows = [
        {"metric": "records_in_candidate_table", "value": len(df)},
        {
            "metric": "rankable_later_count",
            "value": int((df["candidate_review_bucket"] == "rankable_later").sum()),
        },
        {
            "metric": "needs_review_count",
            "value": int((df["candidate_review_bucket"] == "needs_review").sum()),
        },
        {
            "metric": "hold_count",
            "value": int((df["candidate_review_bucket"] == "hold").sum()),
        },
        {
            "metric": "reject_count",
            "value": int((df["candidate_review_bucket"] == "reject").sum()),
        },
        {
            "metric": "missing_price_count",
            "value": int(df["missing_price"].sum()),
        },
        {
            "metric": "missing_square_feet_count",
            "value": int(df["missing_square_feet"].sum()),
        },
        {
            "metric": "missing_lat_long_count",
            "value": int(df["missing_lat_long"].sum()),
        },
        {
            "metric": "undisclosed_address_count",
            "value": int(df["undisclosed_address"].sum()),
        },
        {
            "metric": "outside_target_radius_count",
            "value": int(df["outside_target_radius"].fillna(False).sum()),
        },
        {
            "metric": "overall_scoring_ready_count",
            "value": int(df["overall_scoring_ready"].sum()),
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    """Create active-listing candidate table outputs."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}. "
            "Run scripts/build_property_database.py first."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    normalized_df = pd.read_csv(INPUT_PATH)
    candidate_df = create_active_listing_candidate_table(normalized_df)
    summary_df = create_summary(candidate_df)

    candidate_df.to_csv(OUTPUT_PATH, index=False)
    summary_df.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved active-listing candidate table to: {OUTPUT_PATH}")
    print(f"Saved active-listing candidate summary to: {SUMMARY_PATH}")
    print()
    print("Candidate bucket summary:")
    print(
        candidate_df["candidate_review_bucket"]
        .value_counts(dropna=False)
        .to_string()
    )
    print()
    print("Preview:")
    print(
        candidate_df[
            [
                "address",
                "home_type",
                "price",
                "square_feet",
                "price_per_sqft",
                "distance_from_02131_miles",
                "candidate_state",
                "candidate_review_bucket",
                "overall_scoring_ready",
            ]
        ].head(20).to_string(index=False)
    )


if __name__ == "__main__":
    main()