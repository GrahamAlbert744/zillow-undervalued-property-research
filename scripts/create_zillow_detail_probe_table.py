"""
Create structured Zillow detail-probe tables.

Purpose:
- Store manually observed Zillow Zestimate / Rent Zestimate probe results.
- Keep detail-field validation separate from search-level Zillow output.
- Prepare for a future parser without building scoring yet.

Inputs:
- Manual observations from Zillow connector detail calls.

Outputs:
- data/interim/zillow_detail_probe_results.csv
- outputs/tables/zillow_detail_probe_summary.csv
"""

from pathlib import Path

import pandas as pd


DETAIL_PROBE_RESULTS = [
    {
        "probe_date": "2026-06-25",
        "property_id": "59147121",
        "zpid": "59147121",
        "address": "41 Brown Ave, Roslindale, MA 02131",
        "property_type": "single_family",
        "listing_price": 1650000,
        "zestimate": 1606400,
        "zestimate_per_sqft": 515,
        "zestimate_range_low": 1526000,
        "zestimate_range_high": 1687000,
        "rent_zestimate": 5023,
        "beds": 5,
        "baths": 3,
        "square_feet": 3117,
        "year_built": 1885,
        "zestimate_returned": True,
        "rent_zestimate_returned": True,
        "comps_returned": True,
        "seller_listing_price_key_input": True,
        "notes": "Single-family test property. Zestimate and Rent Zestimate returned.",
    },
    {
        "probe_date": "2026-06-25",
        "property_id": "59210672",
        "zpid": "59210672",
        "address": "15 S Fairview St #3, Roslindale, MA 02131",
        "property_type": "condo",
        "listing_price": 583500,
        "zestimate": 579600,
        "zestimate_per_sqft": 393,
        "zestimate_range_low": 551000,
        "zestimate_range_high": 609000,
        "rent_zestimate": 3488,
        "beds": 3,
        "baths": 1,
        "square_feet": 1475,
        "year_built": 1900,
        "zestimate_returned": True,
        "rent_zestimate_returned": True,
        "comps_returned": True,
        "seller_listing_price_key_input": True,
        "notes": "Condo test property. Zestimate and Rent Zestimate returned.",
    },
    {
        "probe_date": "2026-06-25",
        "property_id": "59141211",
        "zpid": "59141211",
        "address": "45 Harrison St APT B, Roslindale, MA 02131",
        "property_type": "townhome",
        "listing_price": 599900,
        "zestimate": 595500,
        "zestimate_per_sqft": 344,
        "zestimate_range_low": 566000,
        "zestimate_range_high": 625000,
        "rent_zestimate": 3834,
        "beds": 3,
        "baths": 3,
        "square_feet": 1731,
        "year_built": 1988,
        "zestimate_returned": True,
        "rent_zestimate_returned": True,
        "comps_returned": True,
        "seller_listing_price_key_input": True,
        "notes": "Townhouse test property. Zestimate and Rent Zestimate returned.",
    },
    {
        "probe_date": "2026-06-25",
        "property_id": "190036074",
        "zpid": "190036074",
        "address": "74-76 Poplar St, Roslindale, MA 02131",
        "property_type": "multi_family",
        "listing_price": 1190000,
        "zestimate": 1178500,
        "zestimate_per_sqft": 304,
        "zestimate_range_low": 1120000,
        "zestimate_range_high": 1237000,
        "rent_zestimate": 4338,
        "beds": 9,
        "baths": 3,
        "square_feet": 3876,
        "year_built": 1905,
        "zestimate_returned": True,
        "rent_zestimate_returned": True,
        "comps_returned": True,
        "seller_listing_price_key_input": True,
        "notes": "Multifamily test property. Zestimate and Rent Zestimate returned.",
    },
]


def create_detail_probe_dataframe() -> pd.DataFrame:
    """Create dataframe from detail-probe observations."""
    df = pd.DataFrame(DETAIL_PROBE_RESULTS)

    df["annual_rent_zestimate"] = df["rent_zestimate"] * 12
    df["gross_rent_yield"] = df["annual_rent_zestimate"] / df["listing_price"]

    df["price_to_zestimate_pct"] = (
        (df["listing_price"] - df["zestimate"]) / df["zestimate"]
    )

    df["zestimate_range_width"] = (
        df["zestimate_range_high"] - df["zestimate_range_low"]
    )

    df["zestimate_range_width_pct"] = (
        df["zestimate_range_width"] / df["zestimate"]
    )

    df["detail_data_needs_review"] = False

    return df


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary table for detail probe."""
    rows = [
        {
            "metric": "properties_tested",
            "value": len(df),
        },
        {
            "metric": "zestimate_returned_count",
            "value": int(df["zestimate_returned"].sum()),
        },
        {
            "metric": "rent_zestimate_returned_count",
            "value": int(df["rent_zestimate_returned"].sum()),
        },
        {
            "metric": "comps_returned_count",
            "value": int(df["comps_returned"].sum()),
        },
        {
            "metric": "seller_listing_price_key_input_count",
            "value": int(df["seller_listing_price_key_input"].sum()),
        },
        {
            "metric": "median_gross_rent_yield",
            "value": round(float(df["gross_rent_yield"].median()), 4),
        },
        {
            "metric": "median_price_to_zestimate_pct",
            "value": round(float(df["price_to_zestimate_pct"].median()), 4),
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    interim_dir = Path("data/interim")
    output_dir = Path("outputs/tables")

    interim_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    detail_path = interim_dir / "zillow_detail_probe_results.csv"
    summary_path = output_dir / "zillow_detail_probe_summary.csv"

    df = create_detail_probe_dataframe()
    summary = create_summary(df)

    df.to_csv(detail_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Saved detail probe results to: {detail_path}")
    print(f"Saved detail probe summary to: {summary_path}")
    print()
    print("Detail probe preview:")
    print(
        df[
            [
                "address",
                "property_type",
                "listing_price",
                "zestimate",
                "rent_zestimate",
                "gross_rent_yield",
                "price_to_zestimate_pct",
            ]
        ].to_string(index=False)
    )
    print()
    print("Summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()