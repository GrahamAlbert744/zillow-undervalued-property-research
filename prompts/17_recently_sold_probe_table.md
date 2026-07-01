# Prompt 17 — Create Recently Sold Probe Table

## Phase

Phase 12C

## Purpose

Structure recently sold search observations into local CSV outputs.

## What to build

A script that creates recently sold probe tables.

## Zillow data to inspect or pull

Manual observations from recently sold search and widget-state audit.

## Files to create or update

- `scripts/create_recently_sold_probe_table.py`
- `data/interim/recently_sold_probe_results.csv`
- `outputs/tables/recently_sold_probe_summary.csv`

## Inputs

Manual recently sold observations.

## Outputs

Recently sold probe results and summary.

## Acceptance criteria

- Stores sold-search fields separately from active-listing fields.
- Calculates sold price per square foot.
- Calculates distance from 02131.
- Adds sale-outcome validation flags.
- Does not backtest.

## Data-quality checks

- status conflict flag
- outside radius
- sale date availability
- final sale price confirmation
- missing price/square feet

## Correction / refinement step

If CSV is missing, rerun the script and confirm `data/interim/recently_sold_probe_results.csv`.

## Prompt text

```text
Create a structured recently sold probe table for the Zillow undervalued-property research project.

Create:
- scripts/create_recently_sold_probe_table.py
- data/interim/recently_sold_probe_results.csv
- outputs/tables/recently_sold_probe_summary.csv

The table should include:
- probe_date
- property_id
- zpid
- address
- city
- state
- zip_code
- sold_search_price
- sold_price_per_sqft
- status_type
- status_text
- nested_home_status
- home_type
- beds
- baths
- square_feet
- lot_size
- lot_size_units
- latitude
- longitude
- distance_from_02131_miles
- outside_target_radius
- zestimate
- rent_zestimate
- zillow_url
- status_conflict_flag
- sale_outcome_needs_validation
- sale_date_available
- price_history_available
- original_list_price_available
- final_sale_price_confirmed

Rules:
- Do not treat sold_search_price as confirmed final sale price.
- Set sale_outcome_needs_validation = True.
- Set final_sale_price_confirmed = False unless explicitly confirmed.
- Do not build backtesting.
```
