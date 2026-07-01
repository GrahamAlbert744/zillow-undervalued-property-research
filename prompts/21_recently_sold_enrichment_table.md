# Prompt 21 — Create Recently Sold Enrichment Probe Table

## Phase

Phase 12G

## Purpose

Combine recently sold search, detail, Zestimate-history, and Rent Zestimate observations into one enrichment table.

## What to build

A local coding phase, not a Zillow probe.

## Zillow data to inspect or pull

Use previously observed Phase 12A–12F outputs.

## Files to create or update

- `scripts/create_recently_sold_enrichment_probe_table.py`
- `data/interim/recently_sold_enrichment_probe_results.csv`
- `outputs/tables/recently_sold_enrichment_probe_summary.csv`
- `docs/data_dictionary.md`

## Inputs

Manual observations from recently sold probes.

## Outputs

Recently sold enrichment table and summary.

## Acceptance criteria

- Combines search fields, tax/parcel availability, Zestimate-history availability, Rent Zestimate availability.
- Preserves sale-outcome validation flags.
- Does not backtest.
- Does not mark final sale price confirmed.

## Data-quality checks

- sale_date_available = False unless confirmed
- final_sale_price_confirmed = False unless confirmed
- sale_outcome_needs_validation = True
- rent_zestimate_available
- zestimate_history_available
- tax_detail_available
- tax_assessed_value_available
- parcel_id_available

## Correction / refinement step

If any source value is uncertain, add a validation flag rather than treating it as confirmed.

## Prompt text

```text
Create a recently sold enrichment probe table for the Zillow undervalued-property research project.

Create:
- scripts/create_recently_sold_enrichment_probe_table.py
- data/interim/recently_sold_enrichment_probe_results.csv
- outputs/tables/recently_sold_enrichment_probe_summary.csv

Use the manually observed results from:
- recently sold search
- recently sold widget-state audit
- recently sold detail validation
- Zestimate-history validation
- Rent Zestimate validation

Include:
- property_id
- zpid
- address
- city
- state
- zip_code
- home_type
- sold_search_price
- sold_price_per_sqft
- beds
- baths
- square_feet
- latitude
- longitude
- distance_from_02131_miles
- outside_target_radius
- status_type
- status_text
- nested_home_status
- status_conflict_flag
- current_zestimate
- zestimate_history_available
- zestimate_history_start_date
- zestimate_history_end_date
- zestimate_pct_change_latest
- zestimate_pct_change_min
- zestimate_pct_change_max
- rent_zestimate
- rent_zestimate_available
- annual_rent_zestimate
- gross_rent_yield_using_sold_search_price
- tax_detail_available
- tax_assessed_value_available
- parcel_id_available
- county_available
- county_fips_available
- tax_history_available
- foreclosure_flag_available
- sale_date_available
- final_sale_price_confirmed
- sale_outcome_needs_validation
- zillow_url
- notes

Rules:
- Do not backtest.
- Do not treat sold_search_price as confirmed final sale price.
- Set sale_outcome_needs_validation = True.
- Preserve uncertainty flags.
```
