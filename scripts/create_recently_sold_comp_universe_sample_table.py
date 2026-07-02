"""
Create recently sold comparable-universe sample table.

Purpose:
- Store selected recently sold Zillow search-level records for Roslindale / ZIP 02131.
- Preserve connector pull metadata.
- Create conservative validation flags.
- Support future comparable-sales context without building scoring or backtesting.

Important:
- Do NOT treat sold_search_price as confirmed final sale price.
- Do NOT infer sale date.
- Do NOT build a comp valuation model yet.

Outputs:
- data/interim/recently_sold_comp_universe_sample.csv
- outputs/tables/recently_sold_comp_universe_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.geocoding import haversine_distance_miles, is_outside_radius
except ModuleNotFoundError:
    from geocoding import haversine_distance_miles, is_outside_radius


PULL_DATE = "2026-07-02"
SEARCH_AREA = "Roslindale / ZIP 02131"
SEARCH_STATUS = "recently_sold"
PROPERTY_TYPES_REQUESTED = "single_family, condo, townhome, multi_family"
TOTAL_MATCHING_COUNT = 792
DISPLAYED_RESULT_COUNT = 100


RECENTLY_SOLD_COMP_SAMPLE = [
    {
        "address": "214 Florence St #1A",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "townhome",
        "sold_search_price": 475000,
        "beds": 3,
        "baths": 2,
        "square_feet": 1074,
        "lot_size": 1074,
        "lot_size_units": "Square Feet",
        "fixture_classification": "unit",
        "title": "Dale Village Condominium",
        "latitude": 42.28665,
        "longitude": -71.12012,
        "zillow_url": "https://www.zillow.com/homedetails/214-Florence-St-1A-Roslindale-MA-02131/462327971_zpid",
    },
    {
        "address": "21 Stella Rd",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 640000,
        "beds": 2,
        "baths": 2,
        "square_feet": 1066,
        "lot_size": 2910,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.2812,
        "longitude": -71.117455,
        "zillow_url": "https://www.zillow.com/homedetails/21-Stella-Rd-Roslindale-MA-02131/59146665_zpid",
    },
    {
        "address": "338 Beech St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 1162000,
        "beds": 3,
        "baths": 3,
        "square_feet": 1800,
        "lot_size": 6174,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.27933,
        "longitude": -71.13831,
        "zillow_url": "https://www.zillow.com/homedetails/338-Beech-St-Roslindale-MA-02131/59144547_zpid",
    },
    {
        "address": "41 Mount Hope St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 640000,
        "beds": 3,
        "baths": 1,
        "square_feet": 1616,
        "lot_size": 5747,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.283825,
        "longitude": -71.117424,
        "zillow_url": "https://www.zillow.com/homedetails/41-Mount-Hope-St-Roslindale-MA-02131/59146714_zpid",
    },
    {
        "address": "951 Canterbury St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "multi_family",
        "sold_search_price": 775000,
        "beds": 4,
        "baths": 3,
        "square_feet": 2446,
        "lot_size": 6478,
        "lot_size_units": "Square Feet",
        "fixture_classification": "unit",
        "title": None,
        "latitude": 42.278755,
        "longitude": -71.11759,
        "zillow_url": "https://www.zillow.com/homedetails/951-Canterbury-St-Roslindale-MA-02131/59213034_zpid",
    },
    {
        "address": "52 Walter St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 1200000,
        "beds": 3,
        "baths": 3,
        "square_feet": 1868,
        "lot_size": 6080,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.290524,
        "longitude": -71.13303,
        "zillow_url": "https://www.zillow.com/homedetails/52-Walter-St-Roslindale-MA-02131/59142138_zpid",
    },
    {
        "address": "11 Eugenia Rd",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 927000,
        "beds": 2,
        "baths": 2,
        "square_feet": 1750,
        "lot_size": 4400,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.279408,
        "longitude": -71.137726,
        "zillow_url": "https://www.zillow.com/homedetails/11-Eugenia-Rd-Roslindale-MA-02131/59144560_zpid",
    },
    {
        "address": "41 Cornell St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 980000,
        "beds": 3,
        "baths": 2,
        "square_feet": 1720,
        "lot_size": 6915,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.276,
        "longitude": -71.12995,
        "zillow_url": "https://www.zillow.com/homedetails/41-Cornell-St-Roslindale-MA-02131/59145429_zpid",
    },
    {
        "address": "602 Canterbury St #6",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "townhome",
        "sold_search_price": 505154,
        "beds": 2,
        "baths": 2,
        "square_feet": 1251,
        "lot_size": None,
        "lot_size_units": None,
        "fixture_classification": "unit",
        "title": "The Canterbury",
        "latitude": 42.2876,
        "longitude": -71.10922,
        "zillow_url": "https://www.zillow.com/homedetails/602-Canterbury-St-6-Roslindale-MA-02131/458870441_zpid",
    },
    {
        "address": "63 Bradwood St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "multi_family",
        "sold_search_price": 1200000,
        "beds": 5,
        "baths": 3,
        "square_feet": 3388,
        "lot_size": 5500,
        "lot_size_units": "Square Feet",
        "fixture_classification": "unit",
        "title": None,
        "latitude": 42.284805,
        "longitude": -71.14343,
        "zillow_url": "https://www.zillow.com/homedetails/63-Bradwood-St-Roslindale-MA-02131/59143738_zpid",
    },
    {
        "address": "209 Beech St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "single_family",
        "sold_search_price": 1300000,
        "beds": 3,
        "baths": 3,
        "square_feet": 2534,
        "lot_size": 6120,
        "lot_size_units": "Square Feet",
        "fixture_classification": "improvement",
        "title": None,
        "latitude": 42.281384,
        "longitude": -71.14219,
        "zillow_url": "https://www.zillow.com/homedetails/209-Beech-St-Roslindale-MA-02131/59147362_zpid",
    },
    {
        "address": "122 Aldrich St",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "home_type": "multi_family",
        "sold_search_price": 1015000,
        "beds": 7,
        "baths": 2,
        "square_feet": 2616,
        "lot_size": 4250,
        "lot_size_units": "Square Feet",
        "fixture_classification": "unit",
        "title": None,
        "latitude": 42.282864,
        "longitude": -71.142784,
        "zillow_url": "https://www.zillow.com/homedetails/122-Aldrich-St-Roslindale-MA-02131/59144272_zpid",
    },
]


def create_comp_universe_dataframe() -> pd.DataFrame:
    """Create recently sold comp-universe sample dataframe."""
    df = pd.DataFrame(RECENTLY_SOLD_COMP_SAMPLE)

    df.insert(0, "connector_pull_date", PULL_DATE)
    df.insert(1, "search_area", SEARCH_AREA)
    df.insert(2, "search_status", SEARCH_STATUS)
    df.insert(3, "property_types_requested", PROPERTY_TYPES_REQUESTED)
    df.insert(4, "total_matching_count", TOTAL_MATCHING_COUNT)
    df.insert(5, "displayed_result_count", DISPLAYED_RESULT_COUNT)

    df["property_key"] = (
        df["address"].astype(str)
        + ", "
        + df["city"].astype(str)
        + ", "
        + df["state"].astype(str)
        + " "
        + df["zip_code"].astype(str)
    )

    df["zillow_recently_sold_comp_universe_match"] = True

    df["sold_search_price_per_sqft"] = (
        df["sold_search_price"] / df["square_feet"]
    ).round(2)

    df["distance_from_02131_miles"] = df.apply(
        lambda row: haversine_distance_miles(
            row["latitude"],
            row["longitude"],
        ),
        axis=1,
    ).round(2)

    df["outside_target_radius"] = df["distance_from_02131_miles"].apply(
        is_outside_radius
    )

    # Conservative validation flags.
    df["sold_search_price_needs_validation"] = True
    df["sold_search_price_is_confirmed_final_sale_price"] = False
    df["sale_date_available"] = False
    df["confirmed_sale_date"] = None
    df["final_sale_price_confirmed"] = False
    df["confirmed_final_sale_price"] = None
    df["sale_outcome_needs_validation"] = True
    df["original_list_price_available"] = False
    df["last_list_price_before_sale_available"] = False
    df["days_on_market_available"] = False
    df["price_history_available"] = False
    df["condition_details_available"] = False
    df["true_comp_similarity_score_available"] = False
    df["backtesting_ready"] = False

    df["comp_universe_notes"] = (
        "Recently sold search-level comp-universe record. "
        "Useful for future comparable-sales context, but sale date and final sale price are not confirmed."
    )

    preferred_columns = [
        "connector_pull_date",
        "search_area",
        "search_status",
        "property_types_requested",
        "total_matching_count",
        "displayed_result_count",
        "property_key",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
        "fixture_classification",
        "title",
        "sold_search_price",
        "sold_search_price_per_sqft",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "zillow_recently_sold_comp_universe_match",
        "sold_search_price_needs_validation",
        "sold_search_price_is_confirmed_final_sale_price",
        "sale_date_available",
        "confirmed_sale_date",
        "final_sale_price_confirmed",
        "confirmed_final_sale_price",
        "sale_outcome_needs_validation",
        "original_list_price_available",
        "last_list_price_before_sale_available",
        "days_on_market_available",
        "price_history_available",
        "condition_details_available",
        "true_comp_similarity_score_available",
        "backtesting_ready",
        "zillow_url",
        "comp_universe_notes",
    ]

    return df[preferred_columns]


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary table for recently sold comp-universe sample."""
    rows = [
        {"metric": "connector_pull_date", "value": PULL_DATE},
        {"metric": "search_area", "value": SEARCH_AREA},
        {"metric": "total_matching_count", "value": TOTAL_MATCHING_COUNT},
        {"metric": "displayed_result_count", "value": DISPLAYED_RESULT_COUNT},
        {"metric": "sample_records_stored", "value": len(df)},
        {
            "metric": "single_family_count",
            "value": int((df["home_type"] == "single_family").sum()),
        },
        {
            "metric": "condo_count",
            "value": int((df["home_type"] == "condo").sum()),
        },
        {
            "metric": "townhome_count",
            "value": int((df["home_type"] == "townhome").sum()),
        },
        {
            "metric": "multi_family_count",
            "value": int((df["home_type"] == "multi_family").sum()),
        },
        {
            "metric": "outside_target_radius_count",
            "value": int(df["outside_target_radius"].fillna(False).sum()),
        },
        {
            "metric": "sale_date_available_count",
            "value": int(df["sale_date_available"].sum()),
        },
        {
            "metric": "final_sale_price_confirmed_count",
            "value": int(df["final_sale_price_confirmed"].sum()),
        },
        {
            "metric": "backtesting_ready_count",
            "value": int(df["backtesting_ready"].sum()),
        },
        {
            "metric": "median_sold_search_price",
            "value": round(float(df["sold_search_price"].median()), 2),
        },
        {
            "metric": "median_sold_search_price_per_sqft",
            "value": round(float(df["sold_search_price_per_sqft"].median()), 2),
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    interim_dir = Path("data/interim")
    output_dir = Path("outputs/tables")

    interim_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_path = interim_dir / "recently_sold_comp_universe_sample.csv"
    summary_path = output_dir / "recently_sold_comp_universe_summary.csv"

    df = create_comp_universe_dataframe()
    summary = create_summary(df)

    df.to_csv(sample_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Saved comp-universe sample to: {sample_path}")
    print(f"Saved comp-universe summary to: {summary_path}")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()