# Prompt 18 — Recently Sold Detail Validation

## Phase

Phase 12D

## Purpose

Test whether Zillow detail calls for recently sold/off-market properties return sale-outcome fields or only enrichment fields.

## What to build

Documentation of recently sold detail capabilities.

## Zillow data to inspect or pull

3 recently sold/off-market property addresses.

## Files to create or update

- `docs/zillow_field_notes.md`

## Inputs

Recently sold property addresses.

## Outputs

Detail-call results and missing-field audit.

## Acceptance criteria

- Tests several property types.
- Identifies whether sale date/final sale price are returned.
- Identifies tax/parcel fields returned.
- Does not backtest.

## Data-quality checks

- confirmed final sale price
- sale date
- tax assessed value
- parcel ID
- county/FIPS
- non-owner-occupied flag
- tax history availability

## Correction / refinement step

If sale outcomes are missing, record `sale_outcome_needs_validation = True`.

## Prompt text

```text
For each recently sold or off-market property below, use the Zillow detail tool to test whether richer sale-outcome fields are available.

Properties:
[PASTE 3 RECENTLY SOLD ADDRESSES]

Return all available fields, especially:
- final sale price
- sale date
- original list price
- last list price before sale
- price history
- days on market
- beds
- baths
- square feet
- tax assessed value
- tax assessed year
- property tax rate
- tax history
- parcel ID
- county
- county FIPS
- foreclosure flags
- undisclosed-address flag
- non-owner-occupied flag

Clearly separate:
1. fields returned
2. fields not returned
3. fields requiring validation

Do not backtest.
Do not infer sale outcomes.
```
