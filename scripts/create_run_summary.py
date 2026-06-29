"""
Create run summary report for the Zillow undervalued-property project.

Purpose:
- Summarize the current normalized Zillow property dataset.
- Summarize data-quality results if available.
- Avoid crashing when expected data-quality columns are missing.

Inputs:
- data/processed/all_properties_normalized.csv
- outputs/tables/property_data_quality_flags.csv, if available
- outputs/tables/property_missingness_report.csv, if available
- outputs/tables/property_type_summary.csv, if available

Output:
- outputs/reports/run_summary.md
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


NORMALIZED_PATH = Path("data/processed/all_properties_normalized.csv")
QUALITY_FLAGS_PATH = Path("outputs/tables/property_data_quality_flags.csv")
MISSINGNESS_PATH = Path("outputs/tables/property_missingness_report.csv")
PROPERTY_TYPE_PATH = Path("outputs/tables/property_type_summary.csv")
REPORT_PATH = Path("outputs/reports/run_summary.md")


def read_csv_if_exists(path: Path) -> pd.DataFrame | None:
    """Read CSV if it exists; otherwise return None."""
    if not path.exists():
        return None

    return pd.read_csv(path)


def safe_count_true(df: pd.DataFrame, column: str) -> int:
    """Count True values in a boolean-like column. Return 0 if missing."""
    if column not in df.columns:
        return 0

    return int(df[column].fillna(False).astype(bool).sum())


def safe_nonmissing_count(df: pd.DataFrame, column: str) -> int:
    """Count non-missing values in a column. Return 0 if missing."""
    if column not in df.columns:
        return 0

    return int(df[column].notna().sum())


def safe_missing_count(df: pd.DataFrame, column: str) -> int:
    """Count missing values in a column. Return 0 if missing."""
    if column not in df.columns:
        return 0

    return int(df[column].isna().sum())


def safe_median(df: pd.DataFrame, column: str) -> Any:
    """Return rounded median if column exists and has data."""
    if column not in df.columns:
        return "not available"

    numeric = pd.to_numeric(df[column], errors="coerce")

    if numeric.dropna().empty:
        return "not available"

    return round(float(numeric.median()), 2)


def merge_quality_flags(
    normalized_df: pd.DataFrame,
    quality_df: pd.DataFrame | None,
) -> pd.DataFrame:
    """
    Add quality flag columns to normalized dataframe when available.

    Strategy:
    1. If quality file is missing, add fallback data_needs_review.
    2. If quality file has property_id or zpid, merge by key.
    3. If same number of rows, append missing quality columns positionally.
    4. Otherwise, add fallback data_needs_review.
    """
    df = normalized_df.copy()

    if quality_df is None or quality_df.empty:
        if "data_needs_review" not in df.columns:
            df["data_needs_review"] = False
        return df

    key_candidates = ["property_id", "zpid"]

    for key in key_candidates:
        if key in df.columns and key in quality_df.columns:
            quality_columns = [
                column
                for column in quality_df.columns
                if column not in df.columns or column == key
            ]

            merged = df.merge(
                quality_df[quality_columns],
                on=key,
                how="left",
            )

            if "data_needs_review" not in merged.columns:
                merged["data_needs_review"] = False

            return merged

    if len(df) == len(quality_df):
        for column in quality_df.columns:
            if column not in df.columns:
                df[column] = quality_df[column].values

        if "data_needs_review" not in df.columns:
            df["data_needs_review"] = False

        return df

    if "data_needs_review" not in df.columns:
        df["data_needs_review"] = False

    return df


def build_property_type_section(df: pd.DataFrame) -> str:
    """Create markdown section for property type counts."""
    if "home_type" not in df.columns:
        return "Property type field not available.\n"

    counts = (
        df["home_type"]
        .fillna("missing")
        .value_counts()
        .reset_index()
    )

    counts.columns = ["home_type", "count"]

    lines = ["| Home type | Count |", "|---|---:|"]

    for _, row in counts.iterrows():
        lines.append(f"| {row['home_type']} | {int(row['count'])} |")

    return "\n".join(lines) + "\n"


def build_missingness_section(df: pd.DataFrame) -> str:
    """Create markdown section for key missingness counts."""
    key_columns = [
        "address",
        "price",
        "beds",
        "baths",
        "square_feet",
        "home_type",
        "latitude",
        "longitude",
        "zestimate",
        "rent_zestimate",
        "distance_from_02131_miles",
    ]

    lines = ["| Field | Missing count |", "|---|---:|"]

    for column in key_columns:
        if column in df.columns:
            lines.append(f"| `{column}` | {safe_missing_count(df, column)} |")
        else:
            lines.append(f"| `{column}` | column not available |")

    return "\n".join(lines) + "\n"


def main() -> None:
    if not NORMALIZED_PATH.exists():
        raise FileNotFoundError(
            f"Normalized file not found: {NORMALIZED_PATH}. "
            "Run scripts\\build_property_database.py first."
        )

    normalized_df = pd.read_csv(NORMALIZED_PATH)
    quality_df = read_csv_if_exists(QUALITY_FLAGS_PATH)

    df = merge_quality_flags(normalized_df, quality_df)

    total_records = len(df)
    records_needing_review = safe_count_true(df, "data_needs_review")
    outside_radius_count = safe_count_true(df, "outside_target_radius")
    missing_lat_long_count = safe_count_true(df, "missing_lat_long")

    if missing_lat_long_count == 0:
        missing_lat_long_count = (
            safe_missing_count(df, "latitude")
            + safe_missing_count(df, "longitude")
        )

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "# Zillow Property Pipeline Run Summary",
        "",
        f"Run created: `{run_time}`",
        "",
        "## Purpose",
        "",
        (
            "Summarize the current Zillow property pipeline output. "
            "This report is for data validation and workflow tracking only. "
            "It does not recommend buying or selling any property."
        ),
        "",
        "## Input files",
        "",
        f"- Normalized properties: `{NORMALIZED_PATH}`",
        f"- Data-quality flags: `{QUALITY_FLAGS_PATH}` "
        f"({'found' if QUALITY_FLAGS_PATH.exists() else 'not found'})",
        f"- Missingness report: `{MISSINGNESS_PATH}` "
        f"({'found' if MISSINGNESS_PATH.exists() else 'not found'})",
        f"- Property type summary: `{PROPERTY_TYPE_PATH}` "
        f"({'found' if PROPERTY_TYPE_PATH.exists() else 'not found'})",
        "",
        "## Core counts",
        "",
        f"- Total normalized records: **{total_records}**",
        f"- Records needing review: **{records_needing_review}**",
        f"- Records outside 25-mile radius: **{outside_radius_count}**",
        f"- Records missing latitude/longitude: **{missing_lat_long_count}**",
        "",
        "## Core field availability",
        "",
        f"- Price values available: **{safe_nonmissing_count(df, 'price')}**",
        f"- Square-foot values available: **{safe_nonmissing_count(df, 'square_feet')}**",
        f"- Zestimate values available: **{safe_nonmissing_count(df, 'zestimate')}**",
        f"- Rent Zestimate values available: **{safe_nonmissing_count(df, 'rent_zestimate')}**",
        f"- Distance-from-02131 values available: **{safe_nonmissing_count(df, 'distance_from_02131_miles')}**",
        "",
        "## Median metrics",
        "",
        f"- Median listing price: **{safe_median(df, 'price')}**",
        f"- Median square feet: **{safe_median(df, 'square_feet')}**",
        f"- Median price per sqft: **{safe_median(df, 'price_per_sqft')}**",
        f"- Median distance from 02131: **{safe_median(df, 'distance_from_02131_miles')} miles**",
        "",
        "## Property type counts",
        "",
        build_property_type_section(df),
        "",
        "## Missingness summary",
        "",
        build_missingness_section(df),
        "",
        "## Important interpretation notes",
        "",
        "- This pipeline is still pre-scoring.",
        "- Distance validation is now part of the normalized property file if `src/geocoding.py` is available.",
        "- Missing fields should be flagged, not guessed.",
        "- `data_needs_review` may come from the data-quality file rather than the normalized file.",
        "- Properties outside the 25-mile radius should be excluded from future main rankings.",
        "",
        "## Next recommended step",
        "",
        (
            "Confirm that `distance_from_02131_miles` and `outside_target_radius` "
            "are present in `all_properties_normalized.csv`, then update "
            "`docs/data_dictionary.md` if needed."
        ),
        "",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    print(f"Saved run summary to: {REPORT_PATH}")
    print(f"Total records: {total_records}")
    print(f"Records needing review: {records_needing_review}")
    print(f"Outside-radius records: {outside_radius_count}")


if __name__ == "__main__":
    main()