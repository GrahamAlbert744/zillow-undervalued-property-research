# Prompt 05 — Build Field Mapping / Normalization Module

## Phase

Phase 9

## Purpose

Normalize raw Zillow connector output into one row per property/listing.

## What to build

A reusable field-mapping module.

## Zillow data to inspect or pull

Local raw sample from `data/raw/`.

## Files to create or update

- `src/field_mapping.py`
- `scripts/build_property_database.py`
- `data/processed/all_properties_normalized.csv`

## Inputs

- `data/raw/zillow_raw_search_YYYYMMDD.json`

## Outputs

- `data/processed/all_properties_normalized.csv`

## Acceptance criteria

- Loads raw JSON.
- Extracts records from supported payload shapes.
- Normalizes key fields.
- Calculates derived fields where safe.
- Exports CSV.
- Does not score properties.

## Data-quality checks

- Check row count.
- Check expected columns exist.
- Check price and square footage are numeric.
- Check ZPID extraction.
- Check address construction.
- Check missing fields remain null, not hallucinated.

## Correction / refinement step

If Zillow connector returns nested shapes, add fallback paths instead of replacing the whole schema.

## Prompt text

```text
Create or revise src/field_mapping.py and scripts/build_property_database.py for my Zillow undervalued-property research project.

Goal:
Load raw Zillow JSON and normalize it into one row per property/listing.

Support both:
1. flat development samples
2. nested Zillow connector search results

Normalize these fields when available:
- property_id
- zpid
- address
- city
- state
- zip_code
- latitude
- longitude
- is_bad_geocode
- home_status
- status_text
- home_type
- fixture_classification
- price
- zestimate
- rent_zestimate
- beds
- baths
- square_feet
- lot_size
- lot_size_units
- price_per_sqft
- price_to_zestimate_pct
- annual_rent_zestimate
- gross_rent_yield
- new_construction_available_plan_count
- new_construction_premier_builder
- has_open_house
- has_vr_model
- title
- zillow_url
- search_date
- data_source

Requirements:
- Use safe parsing functions.
- Do not invent missing fields.
- Keep unavailable values as null.
- Do not build scoring.
- Print a small preview after running.
```
