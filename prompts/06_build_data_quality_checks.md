# Prompt 06 — Build Data-Quality Checks

## Phase

Phase 3 / Phase 9

## Purpose

Create data-quality flags before scoring.

## What to build

A data-quality module and script.

## Zillow data to inspect or pull

Use normalized property dataframe.

## Files to create or update

- `src/data_quality.py`
- `scripts/run_data_quality_check.py`
- `outputs/tables/property_missingness_report.csv`
- `outputs/tables/property_data_quality_flags.csv`
- `outputs/tables/property_type_summary.csv`
- `outputs/tables/properties_needing_review.csv`

## Inputs

- `data/processed/all_properties_normalized.csv`

## Outputs

Data-quality CSV files in `outputs/tables/`.

## Acceptance criteria

- Adds flags for missing core fields.
- Flags invalid prices and square footage.
- Flags undisclosed addresses.
- Flags duplicate addresses and duplicate lat/long.
- Writes all expected reports.
- Does not score properties.

## Data-quality checks

- Missing price
- Missing square feet
- Missing beds
- Missing baths
- Missing home type
- Missing lat/long
- Missing Zestimate
- Missing rent Zestimate
- Invalid price
- Invalid square feet
- Duplicate address
- Duplicate lat/long
- Outside radius, if available
- Data needs review

## Correction / refinement step

If a field is missing from the dataframe, create a safe default instead of crashing.

## Prompt text

```text
Create data-quality checks for the Zillow undervalued-property research project.

Create or update:
- src/data_quality.py
- scripts/run_data_quality_check.py

Input:
- data/processed/all_properties_normalized.csv

Outputs:
- outputs/tables/property_missingness_report.csv
- outputs/tables/property_data_quality_flags.csv
- outputs/tables/property_type_summary.csv
- outputs/tables/properties_needing_review.csv

Flags:
- missing_price
- missing_square_feet
- missing_beds
- missing_baths
- missing_home_type
- missing_lat_long
- missing_zestimate
- missing_rent_zestimate
- undisclosed_address
- invalid_price
- invalid_square_feet
- possible_duplicate_address
- possible_duplicate_lat_long
- outside_target_radius, if column exists
- data_needs_review

Rules:
- Do not crash if optional columns are missing.
- Do not delete records automatically.
- Preserve review queues.
- Do not build scoring yet.
```
