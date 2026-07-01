# Prompt 20 — Recently Sold Rent Zestimate Probe

## Phase

Phase 12F

## Purpose

Test whether Rent Zestimate values are available for recently sold/off-market properties.

## What to build

Documentation of rent-estimate availability for enrichment.

## Zillow data to inspect or pull

Rent Zestimate values for 3 recently sold/off-market properties.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: enrichment probe table

## Inputs

Recently sold/off-market property addresses.

## Outputs

Rent Zestimate values and disclaimer text.

## Acceptance criteria

- Returns rent estimates when available.
- Stores availability flags.
- Does not treat Rent Zestimate as confirmed market rent.

## Data-quality checks

- rent estimate available
- missing rent range
- no expense assumptions
- no vacancy assumptions
- no unit-level rent breakdown

## Correction / refinement step

If rent estimate is missing, set `rent_zestimate_available = False` and do not calculate yield.

## Prompt text

```text
For each recently sold or off-market property below, retrieve Zillow Rent Zestimate data if available.

Properties:
[PASTE ADDRESSES]

Return:
- address
- Rent Zestimate
- whether Rent Zestimate is available
- any rent range, if available
- any rent-history data, if available
- any disclaimer text

Do not treat Rent Zestimate as confirmed market rent.
Do not backtest.
Do not infer sale outcomes.
```
