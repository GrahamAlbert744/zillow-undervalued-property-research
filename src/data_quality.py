"""
Data-quality checks for normalized Zillow property data.

This module inspects the normalized dataframe and creates simple
quality-control summaries before any scoring is attempted.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


CORE_FIELDS = [
    "property_id",
    "address",
    "city",
    "state",
    "zip_code",
    "latitude",
    "longitude",
    "home_type",
    "price",
    "beds",
    "baths",
    "square_feet",
    "zillow_url",
]


FLAG_FIELDS = [
    "missing_price",
    "missing_square_feet",
    "missing_beds",
    "missing_baths",
    "missing_home_type",
    "missing_lat_long",
    "missing_zestimate",
    "missing_rent_zestimate",
    "undisclosed_address",
    "invalid_price",
    "invalid_square_feet",
    "possible_duplicate_address",
    "possible_duplicate_lat_long",
    "data_needs_review",
]


def load_normalized_properties(path: str | Path) -> pd.DataFrame:
    """Load normalized property CSV."""
    path = Path(path)
    return pd.read_csv(path)


def summarize_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Create missingness summary for all columns."""
    total_rows = len(df)

    rows = []
    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        missing_pct = missing_count / total_rows if total_rows else 0

        rows.append(
            {
                "field": col,
                "missing_count": missing_count,
                "missing_pct": round(missing_pct, 4),
            }
        )

    return pd.DataFrame(rows).sort_values(
        by=["missing_count", "field"],
        ascending=[False, True],
    )


def summarize_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize boolean data-quality flags."""
    rows = []

    for flag in FLAG_FIELDS:
        if flag not in df.columns:
            rows.append(
                {
                    "flag": flag,
                    "exists": False,
                    "count_true": None,
                    "pct_true": None,
                }
            )
            continue

        count_true = int(df[flag].fillna(False).astype(bool).sum())
        pct_true = count_true / len(df) if len(df) else 0

        rows.append(
            {
                "flag": flag,
                "exists": True,
                "count_true": count_true,
                "pct_true": round(pct_true, 4),
            }
        )

    return pd.DataFrame(rows)


def summarize_property_types(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize property counts by home type."""
    if "home_type" not in df.columns:
        return pd.DataFrame(columns=["home_type", "count"])

    return (
        df["home_type"]
        .fillna("missing")
        .value_counts()
        .reset_index()
        .rename(columns={"index": "home_type", "home_type": "count"})
    )


def find_records_needing_review(df: pd.DataFrame) -> pd.DataFrame:
    """Return records that need manual review."""
    if "data_needs_review" not in df.columns:
        return pd.DataFrame()

    review_cols = [
        col
        for col in [
            "property_id",
            "address",
            "city",
            "home_type",
            "price",
            "beds",
            "baths",
            "square_feet",
            "latitude",
            "longitude",
            "zillow_url",
            "data_needs_review",
            "missing_lat_long",
            "undisclosed_address",
            "possible_duplicate_address",
            "possible_duplicate_lat_long",
        ]
        if col in df.columns
    ]

    return df.loc[df["data_needs_review"] == True, review_cols].copy()


def save_quality_outputs(
    df: pd.DataFrame,
    output_dir: str | Path = "outputs/tables",
) -> None:
    """Save data-quality output tables."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    missingness = summarize_missingness(df)
    flags = summarize_flags(df)
    property_types = summarize_property_types(df)
    needs_review = find_records_needing_review(df)

    missingness.to_csv(output_dir / "property_missingness_report.csv", index=False)
    flags.to_csv(output_dir / "property_data_quality_flags.csv", index=False)
    property_types.to_csv(output_dir / "property_type_summary.csv", index=False)
    needs_review.to_csv(output_dir / "properties_needing_review.csv", index=False)

    print(f"Rows inspected: {len(df)}")
    print(f"Columns inspected: {len(df.columns)}")
    print(f"Records needing review: {len(needs_review)}")
    print(f"Saved quality outputs to: {output_dir}")