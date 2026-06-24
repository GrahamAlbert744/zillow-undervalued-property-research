"""
Build the first normalized property dataframe.

Input:
- data/raw/zillow_raw_search_20260624.json

Output:
- data/processed/all_properties_normalized.csv
"""

from pathlib import Path
import sys

# Make project root importable when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.field_mapping import (
    load_zillow_raw_json,
    normalize_zillow_payload,
    save_normalized_csv,
)

RAW_PATH = Path("data/raw/zillow_raw_search_20260624.json")
OUTPUT_PATH = Path("data/processed/all_properties_normalized.csv")


def main() -> None:
    payload = load_zillow_raw_json(RAW_PATH)
    df = normalize_zillow_payload(payload)

    save_normalized_csv(df, OUTPUT_PATH)

    print(f"Loaded raw records: {len(payload.get('results', []))}")
    print(f"Normalized rows: {len(df)}")
    print(f"Saved normalized CSV to: {OUTPUT_PATH}")

    print("\nColumns:")
    for col in df.columns:
        print(f"- {col}")

    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    main()