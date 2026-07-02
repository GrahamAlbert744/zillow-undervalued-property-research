"""
Create recently sold enrichment probe tables.

Purpose:
- Combine recently sold search-level fields with observed enrichment availability.
- Preserve tax/parcel detail availability.
- Preserve Zestimate-history availability.
- Preserve Rent Zestimate availability.
- Preserve conservative sale-outcome validation flags.
- Do NOT build scoring.
- Do NOT build backtesting.
- Do NOT treat sold-search price as confirmed final sale price.

Outputs:
- data/interim/recently_sold_enrichment_probe_results.csv
- outputs/tables/recently_sold_enrichment_probe_summary.csv
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


RECENTLY_SOLD_ENRICHMENT_RESULTS = [
    {
        "probe_date": "2026-06-29",
        "property_id": "59144560",
        "zpid": "59144560",
        "address": "11 Eugenia Rd, Roslindale, MA 02131",
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
        "latitude": 42.279408,
        "longitude": -71.137726,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "zillow_url": "https://www.zillow.com/homedetails/11-Eugenia-Rd-Roslindale-MA-02131/59144560_zpid",

        # Recently sold detail validation
        "recently_sold_search_available": True,
        "recently_sold_detail_available": True,
        "tax_detail_available": True,
        "parcel_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "undisclosed_address_flag_available": True,
        "non_owner_occupied_flag_available": True,

        # Specific tax/parcel fields observed as available in detail payloads.
        # Values are not stored unless cleanly confirmed.
        "parcel_id_available": True,
        "county_available": True,
        "county_fips_available": True,
        "tax_assessed_value_available": True,
        "tax_assessed_year_available": True,
        "property_tax_rate_available": True,
        "parcel_id": None,
        "county": None,
        "county_fips": None,
        "tax_assessed_value": None,
        "tax_assessed_year": None,
        "property_tax_rate": None,

        # Zestimate-history validation
        "zestimate_history_available": True,
        "current_zestimate": 834900,
        "zestimate_history_start_date": "2021-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "zestimate_history_needs_validation": True,

        # Rent Zestimate validation
        "rent_zestimate_available": True,
        "rent_zestimate": 3294,
        "rent_zestimate_needs_validation": True,
    },
    {
        "probe_date": "2026-06-29",
        "property_id": "57438428",
        "zpid": "57438428",
        "address": "114 Curve St, Dedham, MA 02026",
        "city": "Dedham",
        "state": "MA",
        "zip_code": "02026",
        "home_type": "single_family",
        "sold_search_price": 785000,
        "beds": 3,
        "baths": 2,
        "square_feet": 1524,
        "lot_size": 0.5705693296602388,
        "lot_size_units": "Acres",
        "latitude": 42.252098,
        "longitude": -71.16033,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "zillow_url": "https://www.zillow.com/homedetails/114-Curve-St-Dedham-MA-02026/57438428_zpid",

        "recently_sold_search_available": True,
        "recently_sold_detail_available": True,
        "tax_detail_available": True,
        "parcel_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "undisclosed_address_flag_available": True,
        "non_owner_occupied_flag_available": True,

        "parcel_id_available": True,
        "county_available": True,
        "county_fips_available": True,
        "tax_assessed_value_available": True,
        "tax_assessed_year_available": True,
        "property_tax_rate_available": True,
        "parcel_id": None,
        "county": None,
        "county_fips": None,
        "tax_assessed_value": None,
        "tax_assessed_year": None,
        "property_tax_rate": None,

        "zestimate_history_available": True,
        "current_zestimate": 808900,
        "zestimate_history_start_date": "2021-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "zestimate_history_needs_validation": True,

        "rent_zestimate_available": True,
        "rent_zestimate": 4123,
        "rent_zestimate_needs_validation": True,
    },
    {
        "probe_date": "2026-06-29",
        "property_id": "56330933",
        "zpid": "56330933",
        "address": "56 School St, Somerville, MA 02143",
        "city": "Somerville",
        "state": "MA",
        "zip_code": "02143",
        "home_type": "multi_family",
        "sold_search_price": 1665000,
        "beds": 6,
        "baths": 4,
        "square_feet": 3186,
        "lot_size": 5250,
        "lot_size_units": "Square Feet",
        "latitude": 42.38411,
        "longitude": -71.10087,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "zillow_url": "https://www.zillow.com/homedetails/56-School-St-Somerville-MA-02143/56330933_zpid",

        "recently_sold_search_available": True,
        "recently_sold_detail_available": True,
        "tax_detail_available": True,
        "parcel_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "undisclosed_address_flag_available": True,
        "non_owner_occupied_flag_available": True,

        "parcel_id_available": True,
        "county_available": True,
        "county_fips_available": True,
        "tax_assessed_value_available": True,
        "tax_assessed_year_available": True,
        "property_tax_rate_available": True,
        "parcel_id": None,
        "county": None,
        "county_fips": None,
        "tax_assessed_value": None,
        "tax_assessed_year": None,
        "property_tax_rate": None,

        "zestimate_history_available": True,
        "current_zestimate": 1610200,
        "zestimate_history_start_date": "2023-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "zestimate_history_needs_validation": True,

        "rent_zestimate_available": True,
        "rent_zestimate": 4784,
        "rent_zestimate_needs_validation": True,
    },
]


def create_enrichment_dataframe() -> pd.DataFrame:
    """Create recently sold enrichment probe dataframe."""
    df = pd.DataFrame(RECENTLY_SOLD_ENRICHMENT_RESULTS)

    df["sold_search_price_per_sqft"] = (
        df["sold_search_price"] / df["square_feet"]
    ).round(2)

    df["annual_rent_zestimate"] = df["rent_zestimate"] * 12

    df["gross_rent_yield_using_sold_search_price"] = (
        df["annual_rent_zestimate"] / df["sold_search_price"]
    ).round(4)

    df["sold_search_price_to_current_zestimate_pct"] = (
        (df["sold_search_price"] - df["current_zestimate"])
        / df["current_zestimate"]
    ).round(4)

    df["distance_from_02131_miles"] = df.apply(
        lambda row: haversine_distance_miles(row["latitude"], row["longitude"]),
        axis=1,
    )

    df["distance_from_02131_miles"] = df["distance_from_02131_miles"].round(2)

    df["outside_target_radius"] = df["distance_from_02131_miles"].apply(
        is_outside_radius
    )

    df["status_conflict_flag"] = (
        df["nested_home_status"].notna()
        & ~df["nested_home_status"].isin(["SOLD", "RECENTLY_SOLD"])
    )

    # Required conservative sale-outcome flags.
    df["sale_date_available"] = False
    df["final_sale_price_confirmed"] = False
    df["sale_outcome_needs_validation"] = True
    df["confirmed_final_sale_price"] = None
    df["confirmed_sale_date"] = None

    # Additional conservative flags.
    df["sold_search_price_needs_validation"] = True
    df["sold_search_price_is_confirmed_final_sale_price"] = False
    df["original_list_price_available"] = False
    df["last_list_price_before_sale_available"] = False
    df["days_on_market_available"] = False
    df["price_history_available"] = False
    df["backtesting_ready"] = False

    df["enrichment_notes"] = (
        "Recently sold search/detail/Zestimate/Rent Zestimate enrichment available; "
        "sale date and final sale price remain unconfirmed."
    )

    return df


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary table for recently sold enrichment probe."""
    rows = [
        {"metric": "properties_enriched", "value": len(df)},
        {
            "metric": "recently_sold_search_available_count",
            "value": int(df["recently_sold_search_available"].sum()),
        },
        {
            "metric": "recently_sold_detail_available_count",
            "value": int(df["recently_sold_detail_available"].sum()),
        },
        {
            "metric": "tax_detail_available_count",
            "value": int(df["tax_detail_available"].sum()),
        },
        {
            "metric": "parcel_detail_available_count",
            "value": int(df["parcel_detail_available"].sum()),
        },
        {
            "metric": "zestimate_history_available_count",
            "value": int(df["zestimate_history_available"].sum()),
        },
        {
            "metric": "rent_zestimate_available_count",
            "value": int(df["rent_zestimate_available"].sum()),
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
            "metric": "sale_outcome_needs_validation_count",
            "value": int(df["sale_outcome_needs_validation"].sum()),
        },
        {
            "metric": "backtesting_ready_count",
            "value": int(df["backtesting_ready"].sum()),
        },
        {
            "metric": "outside_target_radius_count",
            "value": int(df["outside_target_radius"].sum()),
        },
        {
            "metric": "median_sold_search_price",
            "value": round(float(df["sold_search_price"].median()), 2),
        },
        {
            "metric": "median_sold_search_price_per_sqft",
            "value": round(float(df["sold_search_price_per_sqft"].median()), 2),
        },
        {
            "metric": "median_current_zestimate",
            "value": round(float(df["current_zestimate"].median()), 2),
        },
        {
            "metric": "median_rent_zestimate",
            "value": round(float(df["rent_zestimate"].median()), 2),
        },
        {
            "metric": "median_gross_rent_yield_using_sold_search_price",
            "value": round(
                float(df["gross_rent_yield_using_sold_search_price"].median()),
                4,
            ),
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    """Create and save recently sold enrichment probe tables."""
    interim_dir = Path("data/interim")
    output_dir = Path("outputs/tables")

    interim_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    enrichment_path = interim_dir / "recently_sold_enrichment_probe_results.csv"
    summary_path = output_dir / "recently_sold_enrichment_probe_summary.csv"

    df = create_enrichment_dataframe()
    summary = create_summary(df)

    df.to_csv(enrichment_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Saved enrichment probe results to: {enrichment_path}")
    print(f"Saved enrichment probe summary to: {summary_path}")
    print()
    print("Enrichment preview:")
    print(
        df[
            [
                "address",
                "home_type",
                "sold_search_price",
                "current_zestimate",
                "rent_zestimate",
                "tax_detail_available",
                "zestimate_history_available",
                "rent_zestimate_available",
                "sale_date_available",
                "final_sale_price_confirmed",
                "sale_outcome_needs_validation",
                "backtesting_ready",
            ]
        ].to_string(index=False)
    )
    print()
    print("Summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()