"""
Create a simple run summary report for the Zillow property pipeline.

Inputs:
- data/processed/all_properties_normalized.csv
- outputs/tables/property_data_quality_flags.csv
- outputs/tables/property_type_summary.csv

Output:
- outputs/reports/run_summary.md
"""

from pathlib import Path
import sys
from datetime import datetime

import pandas as pd

# Make project root importable when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


NORMALIZED_PATH = Path("data/processed/all_properties_normalized.csv")
QUALITY_FLAGS_PATH = Path("outputs/tables/property_data_quality_flags.csv")
PROPERTY_TYPE_PATH = Path("outputs/tables/property_type_summary.csv")
OUTPUT_PATH = Path("outputs/reports/run_summary.md")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(NORMALIZED_PATH)
    flags = pd.read_csv(QUALITY_FLAGS_PATH)
    property_types = pd.read_csv(PROPERTY_TYPE_PATH)

    total_records = len(df)
    records_needing_review = int(df["data_needs_review"].fillna(False).sum())

    price_min = df["price"].min()
    price_median = df["price"].median()
    price_max = df["price"].max()

    sqft_min = df["square_feet"].min()
    sqft_median = df["square_feet"].median()
    sqft_max = df["square_feet"].max()

    lines = []
    lines.append("# Zillow Pipeline Run Summary")
    lines.append("")
    lines.append(f"Run created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This report summarizes the first Zillow data pipeline run. "
        "The goal is to verify that raw Zillow sample data can be normalized "
        "and checked for basic data-quality issues before any scoring is attempted."
    )
    lines.append("")
    lines.append("## Input and Output Files")
    lines.append("")
    lines.append("- Input raw file: `data/raw/zillow_raw_search_20260624.json`")
    lines.append("- Normalized output: `data/processed/all_properties_normalized.csv`")
    lines.append("- Missingness report: `outputs/tables/property_missingness_report.csv`")
    lines.append("- Quality flags report: `outputs/tables/property_data_quality_flags.csv`")
    lines.append("- Property type summary: `outputs/tables/property_type_summary.csv`")
    lines.append("- Records needing review: `outputs/tables/properties_needing_review.csv`")
    lines.append("")
    lines.append("## Record Counts")
    lines.append("")
    lines.append(f"- Total normalized records: {total_records}")
    lines.append(f"- Records needing manual review: {records_needing_review}")
    lines.append("")
    lines.append("## Price Summary")
    lines.append("")
    lines.append(f"- Minimum price: ${price_min:,.0f}")
    lines.append(f"- Median price: ${price_median:,.0f}")
    lines.append(f"- Maximum price: ${price_max:,.0f}")
    lines.append("")
    lines.append("## Square Footage Summary")
    lines.append("")
    lines.append(f"- Minimum square feet: {sqft_min:,.0f}")
    lines.append(f"- Median square feet: {sqft_median:,.0f}")
    lines.append(f"- Maximum square feet: {sqft_max:,.0f}")
    lines.append("")
    lines.append("## Property Types")
    lines.append("")
    lines.append(property_types.to_markdown(index=False))
    lines.append("")
    lines.append("## Data-Quality Flags")
    lines.append("")
    lines.append(flags.to_markdown(index=False))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "This run confirms that the project can move from raw Zillow sample data "
        "to a normalized dataframe and basic data-quality outputs."
    )
    lines.append("")
    lines.append("Do not score properties yet.")
    lines.append("")
    lines.append("Next recommended step:")
    lines.append("")
    lines.append(
        "Review the normalized CSV and data-quality reports, then update "
        "`docs/data_dictionary.md` and `docs/zillow_field_notes.md` based on what was observed."
    )

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved run summary to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()