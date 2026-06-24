"""
Run first data-quality check on normalized Zillow property data.

Input:
- data/processed/all_properties_normalized.csv

Outputs:
- outputs/tables/property_missingness_report.csv
- outputs/tables/property_data_quality_flags.csv
- outputs/tables/property_type_summary.csv
- outputs/tables/properties_needing_review.csv
"""

from pathlib import Path
import sys

# Make project root importable when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_quality import load_normalized_properties, save_quality_outputs


INPUT_PATH = Path("data/processed/all_properties_normalized.csv")


def main() -> None:
    df = load_normalized_properties(INPUT_PATH)
    save_quality_outputs(df)


if __name__ == "__main__":
    main()