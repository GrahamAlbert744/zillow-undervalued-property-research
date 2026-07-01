# Prompt 07 — Create Run Summary Report

## Phase

Phase 6 / Phase 9

## Purpose

Create a readable Markdown run summary from pipeline outputs.

## What to build

A robust run-summary script.

## Zillow data to inspect or pull

None directly. Uses local outputs.

## Files to create or update

- `scripts/create_run_summary.py`
- `outputs/reports/run_summary.md`

## Inputs

- `data/processed/all_properties_normalized.csv`
- `outputs/tables/property_data_quality_flags.csv`
- `outputs/tables/property_missingness_report.csv`
- `outputs/tables/property_type_summary.csv`

## Outputs

- `outputs/reports/run_summary.md`

## Acceptance criteria

- Does not crash if optional columns are missing.
- Reports number of properties.
- Reports missingness and review counts.
- Reports property type counts.
- Notes that scoring is not yet built.

## Data-quality checks

- Confirm `data_needs_review` exists or safely merge from quality flags.
- Confirm missingness report exists.
- Confirm property type summary exists.

## Correction / refinement step

If `data_needs_review` is missing, read it from quality flags or default safely.

## Prompt text

```text
Create a robust run-summary script for the Zillow undervalued-property research project.

Create or update:
- scripts/create_run_summary.py

Inputs:
- data/processed/all_properties_normalized.csv
- outputs/tables/property_data_quality_flags.csv
- outputs/tables/property_missingness_report.csv
- outputs/tables/property_type_summary.csv

Output:
- outputs/reports/run_summary.md

The report should include:
- run date
- number of normalized records
- count of records needing review
- count with missing price
- count with missing square feet
- count with missing lat/long
- count outside target radius, if available
- median price, if available
- median price per square foot, if available
- property type summary
- top missing fields
- clear note that scoring is not yet implemented

Requirement:
Do not crash if optional fields such as data_needs_review are missing from the normalized dataframe. Merge from the quality flags table when available.
```
