"""
Create recently sold enrichment probe table.

Purpose:
- Combine recently sold search observations with enrichment fields from
  Zillow detail, Zestimate-history, and Rent Zestimate probes.
- Keep sale-outcome fields conservative and unconfirmed.
- Prepare for future lifecycle tracking without building scoring or backtesting.

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

from src.geocoding import haversine_distance_miles, is_outside_radius


INTERIM_OUTPUT_PATH = Path("data/interim/recently_sold_enrichment_probe_results.csv")
SUMMARY_OUTPUT_PATH = Path("outputs/tables/recently_sold_enrichment_probe_summary.csv")


RECENTLY_SOLD_ENRICHMENT_PROBES = [
    {
        "probe_date": "2026-07-02",
        "property_id": "59144560",
        "zpid": "59144560",
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
        "latitude": 42.279408,
        "longitude": -71.137726,
        "parcel_id": "ROSLW20P00563S000",
        "county": "Suffolk County",
        "county_fips": "25025",
        "tax_assessed_value": 623100,
        "tax_assessed_year": 2025,
        "property_tax_rate": 0.65,
        "tax_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "is_bank_owned": False,
        "was_non_retail_auction": False,
        "is_undisclosed_address": False,
        "is_non_owner_occupied": False,
        "current_zestimate": 834900,
        "zestimate_history_available": True,
        "zestimate_history_start_date": "2021-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "rent_zestimate": 3294,
        "rent_zestimate_available": True,
        "zillow_url": "https://www.zillow.com/homedetails/11-Eugenia-Rd-Roslindale-MA-02131/59144560_zpid",
        "notes": "Recently sold/off-market enrichment probe. Search price observed, but final sale price/date not independently confirmed.",
    },
    {
        "probe_date": "2026-07-02",
        "property_id": "57438428",
        "zpid": "57438428",
        "address": "114 Curve St",
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
        "parcel_id": "DEDHM0078L0001",
        "county": "Norfolk County",
        "county_fips": "25021",
        "tax_assessed_value": 650900,
        "tax_assessed_year": 2025,
        "property_tax_rate": 1.02,
        "tax_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "is_bank_owned": False,
        "was_non_retail_auction": False,
        "is_undisclosed_address": False,
        "is_non_owner_occupied": False,
        "current_zestimate": 808900,
        "zestimate_history_available": True,
        "zestimate_history_start_date": "2021-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "rent_zestimate": 4123,
        "rent_zestimate_available": True,
        "zillow_url": "https://www.zillow.com/homedetails/114-Curve-St-Dedham-MA-02026/57438428_zpid",
        "notes": "Recently sold/off-market enrichment probe. Search price observed, but final sale price/date not independently confirmed.",
    },
    {
        "probe_date": "2026-07-02",
        "property_id": "56330933",
        "zpid": "56330933",
        "address": "56 School St",
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
        "parcel_id": "SOMEM52BBL14",
        "county": "Middlesex County",
        "county_fips": "25017",
        "tax_assessed_value": 1328200,
        "tax_assessed_year": 2025,
        "property_tax_rate": 1.01,
        "tax_detail_available": True,
        "tax_history_available": True,
        "foreclosure_flag_available": True,
        "is_bank_owned": False,
        "was_non_retail_auction": False,
        "is_undisclosed_address": False,
        "is_non_owner_occupied": False,
        "current_zestimate": 1610200,
        "zestimate_history_available": True,
        "zestimate_history_start_date": "2023-06-30",
        "zestimate_history_end_date": "2026-05-31",
        "rent_zestimate": 4784,
        "rent_zestimate_available": True,
        "zillow_url": "https://www.zillow.com/homedetails/56-School-St-Somerville-MA-02143/56330933_zpid",
        "notes": "Recently sold/off-market enrichment probe. Search price observed, but final sale price/date not independently confirmed.",
    },
]


def add_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["property_key"] = (
        df["address"].astype(str)
        + ", "
        + df["city"].astype(str)
        + ", "
        + df["state"].astype(str)
        + " "
        + df["zip_code"].astype(str)
    )

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
        lambda row: haversine_distance_miles(
            row.get("latitude"),
            row.get("longitude"),
        ),
        axis=1,
    )

    df["distance_from_02131_miles"] = df["distance_from_02131_miles"].round(2)

    df["outside_target_radius"] = df["distance_from_02131_miles"].apply(
        is_outside_radius
    )

    # Conservative sale-outcome fields.
    df["confirmed_final_sale_price"] = None
    df["confirmed_sale_date"] = None
    df["sale_date_available"] = False
    df["final_sale_price_confirmed"] = False
    df["sale_outcome_needs_validation"] = True

    # Backtesting must remain locked until sale outcomes are confirmed.
    df["eligible_for_backtesting"] = False

    df["enrichment_data_needs_review"] = (
        df["sale_outcome_needs_validation"].fillna(True).astype(bool)
        | df["outside_target_radius"].fillna(False).astype(bool)
        | df["confirmed_final_sale_price"].isna()
        | df["confirmed_sale_date"].isna()
    )

    preferred_columns = [
        "probe_date",
        "property_id",
        "zpid",
        "property_key",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
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
        "parcel_id",
        "county",
        "county_fips",
        "tax_assessed_value",
        "tax_assessed_year",
        "property_tax_rate",
        "tax_detail_available",
        "tax_history_available",
        "foreclosure_flag_available",
        "is_bank_owned",
        "was_non_retail_auction",
        "is_undisclosed_address",
        "is_non_owner_occupied",
        "current_zestimate",
        "zestimate_history_available",
        "zestimate_history_start_date",
        "zestimate_history_end_date",
        "sold_search_price_to_current_zestimate_pct",
        "rent_zestimate",
        "rent_zestimate_available",
        "annual_rent_zestimate",
        "gross_rent_yield_using_sold_search_price",
        "confirmed_final_sale_price",
        "confirmed_sale_date",
        "sale_date_available",
        "final_sale_price_confirmed",
        "sale_outcome_needs_validation",
        "eligible_for_backtesting",
        "enrichment_data_needs_review",
        "zillow_url",
        "notes",
    ]

    return df[preferred_columns]


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = [
        {"metric": "record_count", "value": len(df)},
        {
            "metric": "tax_detail_available_count",
            "value": int(df["tax_detail_available"].sum()),
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
            "metric": "eligible_for_backtesting_count",
            "value": int(df["eligible_for_backtesting"].sum()),
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
            "metric": "median_gross_rent_yield_using_sold_search_price",
            "value": round(
                float(df["gross_rent_yield_using_sold_search_price"].median()),
                4,
            ),
        },
        {
            "metric": "median_distance_from_02131_miles",
            "value": round(float(df["distance_from_02131_miles"].median()), 2),
        },
    ]

    return pd.DataFrame(summary_rows)


def main() -> None:
    INTERIM_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(RECENTLY_SOLD_ENRICHMENT_PROBES)
    df = add_derived_fields(df)

    summary = create_summary(df)

    df.to_csv(INTERIM_OUTPUT_PATH, index=False)
    summary.to_csv(SUMMARY_OUTPUT_PATH, index=False)

    print(f"Saved recently sold enrichment results to: {INTERIM_OUTPUT_PATH}")
    print(f"Saved recently sold enrichment summary to: {SUMMARY_OUTPUT_PATH}")
    print("")
    print("Enrichment preview:")
    print(
        df[
            [
                "property_key",
                "home_type",
                "sold_search_price",
                "current_zestimate",
                "rent_zestimate",
                "gross_rent_yield_using_sold_search_price",
                "sale_outcome_needs_validation",
                "eligible_for_backtesting",
            ]
        ].to_string(index=False)
    )
    print("")
    print("Summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()