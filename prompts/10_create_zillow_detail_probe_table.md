# Prompt 10 — Create Zillow Detail-Probe Table

## Phase

Phase 9B

## Purpose

Turn manual Zestimate/Rent Zestimate detail-probe observations into structured CSV outputs.

## What to build

A script that creates detail-probe tables.

## Zillow data to inspect or pull

Manual values from detail probes.

## Files to create or update

- `scripts/create_zillow_detail_probe_table.py`
- `data/interim/zillow_detail_probe_results.csv`
- `outputs/tables/zillow_detail_probe_summary.csv`

## Inputs

Manually observed detail-probe values.

## Outputs

Structured detail-probe CSV and summary CSV.

## Acceptance criteria

- Stores property ID, address, property type, listing price, Zestimate, Rent Zestimate, range, year built, and flags.
- Calculates gross rent yield.
- Calculates price-to-Zestimate percentage.
- Calculates Zestimate range width.
- Does not build scoring.

## Data-quality checks

- Flag seller listing price as a key Zestimate input when observed.
- Mark comps as returned but requiring parsing.
- Keep detail probe separate from active search-level data.

## Correction / refinement step

If later detail calls return more fields, add columns without overwriting previous observations.

## Prompt text

```text
Create a structured detail-probe table for the Zillow undervalued-property research project.

Create:
- scripts/create_zillow_detail_probe_table.py
- data/interim/zillow_detail_probe_results.csv
- outputs/tables/zillow_detail_probe_summary.csv

The script should store manually observed detail-probe results, including:
- probe_date
- property_id
- zpid
- address
- property_type
- listing_price
- zestimate
- zestimate_per_sqft
- zestimate_range_low
- zestimate_range_high
- rent_zestimate
- beds
- baths
- square_feet
- year_built
- zestimate_returned
- rent_zestimate_returned
- comps_returned
- seller_listing_price_key_input
- notes

Derived fields:
- annual_rent_zestimate
- gross_rent_yield
- price_to_zestimate_pct
- zestimate_range_width
- zestimate_range_width_pct
- detail_data_needs_review

Do not build scoring.
Do not merge this into the active listing table yet.
```
