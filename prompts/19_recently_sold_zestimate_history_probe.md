# Prompt 19 — Recently Sold Zestimate-History Probe

## Phase

Phase 12E

## Purpose

Test whether Zestimate-history data is available for recently sold/off-market properties.

## What to build

Documentation of Zestimate-history availability.

## Zillow data to inspect or pull

Zestimate history for 3 recently sold/off-market properties.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: enrichment probe table

## Inputs

Recently sold/off-market property addresses.

## Outputs

Current Zestimate and monthly percentage-change history.

## Acceptance criteria

- Tests multiple property types.
- Records current Zestimate.
- Records history start/end dates.
- Does not treat Zestimate as ground truth.

## Data-quality checks

- history available
- history start date
- history end date
- latest percent change
- sharp recent changes
- Zillow disclaimer

## Correction / refinement step

If history is unavailable for some property types, add availability flag.

## Prompt text

```text
For each recently sold or off-market property below, retrieve Zillow Zestimate-history data if available.

Properties:
[PASTE ADDRESSES]

Return:
- address
- current Zestimate
- monthly percentage-change history
- start date of history
- end date of history
- latest percent change
- minimum percent change
- maximum percent change
- any Zillow disclaimer text

Do not treat Zestimate as ground truth.
Do not backtest.
Do not infer final sale price or sale date.
```
