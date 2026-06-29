"""
Create structured recently sold Zillow probe tables.

Purpose:
- Store observed recently sold Zillow search results.
- Preserve sold-search fields separately from active-listing fields.
- Prepare for future sale-outcome validation.
- Avoid model backtesting until sale prices and sale dates are validated.

Inputs:
- Manual observations from Zillow recently sold connector search.

Outputs:
- data/interim/recently_sold_probe_results.csv
- outputs/tables/recently_sold_probe_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.geocoding import haversine_distance_miles, is_outside_radius


RECENTLY_SOLD_PROBE_RESULTS = [
    {
        "probe_date": "2026-06-29",
        "zpid": "56068253",
        "address": "55 Thistle St, Lynn, MA 01905",
        "city": "Lynn",
        "state": "MA",
        "zip_code": "01905",
        "sold_search_price": 650000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 1,
        "square_feet": 1032,
        "lot_size": 5205,
        "lot_size_units": "Square Feet",
        "latitude": 42.48212,
        "longitude": -70.96972,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/55-Thistle-St-Lynn-MA-01905/56068253_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56312907",
        "address": "284 Lake Ave, Newton, MA 02461",
        "city": "Newton",
        "state": "MA",
        "zip_code": "02461",
        "sold_search_price": 1780000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 3,
        "square_feet": 2186,
        "lot_size": 5882,
        "lot_size_units": "Square Feet",
        "latitude": 42.323868,
        "longitude": -71.20425,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/284-Lake-Ave-Newton-MA-02461/56312907_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56317474",
        "address": "60 Ashton Ave, Newton, MA 02459",
        "city": "Newton",
        "state": "MA",
        "zip_code": "02459",
        "sold_search_price": 2760000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 5,
        "baths": 5,
        "square_feet": 3532,
        "lot_size": 8780,
        "lot_size_units": "Square Feet",
        "latitude": 42.33551,
        "longitude": -71.201004,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/60-Ashton-Ave-Newton-MA-02459/56317474_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56336534",
        "address": "12 Theresa Rd, Stoneham, MA 02180",
        "city": "Stoneham",
        "state": "MA",
        "zip_code": "02180",
        "sold_search_price": 765000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 1,
        "square_feet": 1440,
        "lot_size": 0.28438934802571164,
        "lot_size_units": "Acres",
        "latitude": 42.48679,
        "longitude": -71.084274,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/12-Theresa-Rd-Stoneham-MA-02180/56336534_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56381499",
        "address": "10 Viking Rd, Winchester, MA 01890",
        "city": "Winchester",
        "state": "MA",
        "zip_code": "01890",
        "sold_search_price": 2549000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 4,
        "baths": 4,
        "square_feet": 5674,
        "lot_size": 0.4598943985307622,
        "lot_size_units": "Acres",
        "latitude": 42.43906,
        "longitude": -71.17073,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/10-Viking-Rd-Winchester-MA-01890/56381499_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56390921",
        "address": "7 Parliament Ln, Woburn, MA 01801",
        "city": "Woburn",
        "state": "MA",
        "zip_code": "01801",
        "sold_search_price": 901000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 3,
        "square_feet": 2605,
        "lot_size": 0.4099862258953168,
        "lot_size_units": "Acres",
        "latitude": 42.45928,
        "longitude": -71.200874,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/7-Parliament-Ln-Woburn-MA-01801/56390921_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56402117",
        "address": "9 Venner Rd, Arlington, MA 02476",
        "city": "Arlington",
        "state": "MA",
        "zip_code": "02476",
        "sold_search_price": 1600000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 4,
        "square_feet": 3259,
        "lot_size": 8311,
        "lot_size_units": "Square Feet",
        "latitude": 42.406445,
        "longitude": -71.16372,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/9-Venner-Rd-Arlington-MA-02476/56402117_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "57438428",
        "address": "114 Curve St, Dedham, MA 02026",
        "city": "Dedham",
        "state": "MA",
        "zip_code": "02026",
        "sold_search_price": 785000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 3,
        "baths": 2,
        "square_feet": 1524,
        "lot_size": 0.5705693296602388,
        "lot_size_units": "Acres",
        "latitude": 42.252098,
        "longitude": -71.16033,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/114-Curve-St-Dedham-MA-02026/57438428_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "59144560",
        "address": "11 Eugenia Rd, Roslindale, MA 02131",
        "city": "Roslindale",
        "state": "MA",
        "zip_code": "02131",
        "sold_search_price": 927000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "single_family",
        "beds": 2,
        "baths": 2,
        "square_feet": 1750,
        "lot_size": 4400,
        "lot_size_units": "Square Feet",
        "latitude": 42.279408,
        "longitude": -71.137726,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/11-Eugenia-Rd-Roslindale-MA-02131/59144560_zpid",
    },
    {
        "probe_date": "2026-06-29",
        "zpid": "56330933",
        "address": "56 School St, Somerville, MA 02143",
        "city": "Somerville",
        "state": "MA",
        "zip_code": "02143",
        "sold_search_price": 1665000,
        "status_type": "SOLD",
        "status_text": "Sold",
        "nested_home_status": None,
        "home_type": "multi_family",
        "beds": 6,
        "baths": 4,
        "square_feet": 3186,
        "lot_size": 5250,
        "lot_size_units": "Square Feet",
        "latitude": 42.38411,
        "longitude": -71.10087,
        "zestimate": None,
        "rent_zestimate": None,
        "zillow_url": "https://www.zillow.com/homedetails/56-School-St-Somerville-MA-02143/56330933_zpid",
    },
]


def create_recently_sold_probe_dataframe() -> pd.DataFrame:
    """Create recently sold probe dataframe."""
    df = pd.DataFrame(RECENTLY_SOLD_PROBE_RESULTS)

    df["property_id"] = df["zpid"]

    df["sold_price_per_sqft"] = (
        df["sold_search_price"] / df["square_feet"]
    ).round(2)

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
        & (df["nested_home_status"] != "RECENTLY_SOLD")
        & (df["nested_home_status"] != "SOLD")
    )

    df["sale_outcome_needs_validation"] = True
    df["sale_date_available"] = False
    df["price_history_available"] = False
    df["original_list_price_available"] = False
    df["final_sale_price_confirmed"] = False

    return df


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary table for recently sold probe."""
    rows = [
        {"metric": "properties_tested", "value": len(df)},
        {
            "metric": "outside_target_radius_count",
            "value": int(df["outside_target_radius"].sum()),
        },
        {
            "metric": "status_conflict_count",
            "value": int(df["status_conflict_flag"].sum()),
        },
        {
            "metric": "sale_outcome_needs_validation_count",
            "value": int(df["sale_outcome_needs_validation"].sum()),
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
            "metric": "median_sold_search_price",
            "value": round(float(df["sold_search_price"].median()), 2),
        },
        {
            "metric": "median_sold_price_per_sqft",
            "value": round(float(df["sold_price_per_sqft"].median()), 2),
        },
        {
            "metric": "median_distance_from_02131_miles",
            "value": round(float(df["distance_from_02131_miles"].median()), 2),
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    interim_dir = Path("data/interim")
    output_dir = Path("outputs/tables")

    interim_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    detail_path = interim_dir / "recently_sold_probe_results.csv"
    summary_path = output_dir / "recently_sold_probe_summary.csv"

    df = create_recently_sold_probe_dataframe()
    summary = create_summary(df)

    df.to_csv(detail_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Saved recently sold probe results to: {detail_path}")
    print(f"Saved recently sold probe summary to: {summary_path}")
    print()
    print("Recently sold probe preview:")
    print(
        df[
            [
                "address",
                "city",
                "home_type",
                "sold_search_price",
                "sold_price_per_sqft",
                "distance_from_02131_miles",
                "outside_target_radius",
                "sale_outcome_needs_validation",
            ]
        ].to_string(index=False)
    )
    print()
    print("Summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()