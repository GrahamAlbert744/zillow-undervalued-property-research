# Prompt 08 — Zillow Property Detail Pull

## Phase

Phase 9A

## Purpose

Test whether separate detail/valuation calls can return Zestimate, Rent Zestimate, description, price history, tax history, sale history, or year built.

## What to build

No local code initially. Document field availability.

## Zillow data to inspect or pull

One selected property at a time.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: `data/interim/zillow_detail_probe_results.csv`

## Inputs

Address or Zillow URL.

## Outputs

Detailed field availability notes.

## Acceptance criteria

- Tests at least 3–5 property types.
- Identifies fields returned and not returned.
- Separates active-listing limitations from off-market capabilities.

## Data-quality checks

- Confirm whether Zestimate depends partly on listing price.
- Confirm whether Rent Zestimate is returned.
- Confirm whether comps are returned.
- Confirm whether sale/tax/history fields are structured or text-only.

## Correction / refinement step

If active-listing detail is unsupported, document the limitation and use search-level fields as MVP base.

## Prompt text

```text
For the following Zillow property URL or address, pull the most detailed property information available.

Property:
[PASTE PROPERTY ADDRESS OR ZILLOW URL]

Return all available fields, especially:
- Zestimate
- Zestimate per square foot
- Zestimate range
- Rent Zestimate
- comparable homes
- listing description
- days on Zillow
- price history
- tax history
- sale history
- year built
- HOA fee
- property tax
- lot size
- listing agent
- brokerage
- listing status
- last updated date
- schools or neighborhood fields, if available

Do not summarize yet.
Do not recommend buying or selling.
Return the raw field structure as completely as possible so I can update my data dictionary.
```
