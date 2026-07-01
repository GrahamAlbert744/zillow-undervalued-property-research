# Prompt 02 — Initial 02131 Demo Search

## Phase

Phase 8 / Phase 9

## Purpose

Test search-level Zillow field availability for active residential listings in ZIP code `02131`.

## What to build

No local code yet. Use the connector result to document available fields.

## Zillow data to inspect or pull

Active residential listings in ZIP `02131`.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: `data/raw/zillow_raw_search_YYYYMMDD.json`

## Inputs

ZIP code `02131`, desired property types, desired listing statuses.

## Outputs

A small list of raw search-level listing records.

## Acceptance criteria

- Returns 10–50 listings.
- Includes property address, price, beds, baths, square feet, home type, latitude/longitude, and Zillow URL when available.
- Identifies missing fields.

## Data-quality checks

- Check for missing lat/long.
- Check for undisclosed addresses.
- Check for duplicate or near-duplicate records.
- Check whether Zestimate, rent Zestimate, DOM, listing text, price history, tax history, and sale history appear.

## Correction / refinement step

If the connector returns only partial fields, document them as missing or detail-pull-required. Do not infer missing values.

## Prompt text

```text
Search Zillow for active residential properties in ZIP code 02131.

Include:
- single-family homes
- condos
- townhomes
- multifamily homes

Listing statuses:
- for sale by agent
- for sale by owner
- coming soon, if supported
- new construction

Return up to 25–50 results.

For each property, return all available raw search-level fields, especially:
- address
- city
- state
- ZIP code
- latitude
- longitude
- price
- beds
- baths
- square feet
- lot size
- lot size units
- property type
- listing status
- new construction indicator
- open house indicator
- Zillow URL

Do not score properties.
Do not recommend properties.
The goal is only to inspect available fields and identify missing or unreliable fields.
```
