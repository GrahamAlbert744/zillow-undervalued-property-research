# Prompt 13 — Active Listing Detail Limitation Probe

## Phase

Phase 10C

## Purpose

Test whether Zillow detail calls work for active listings that appear in the price-reduction search.

## What to build

Documentation of detail-call support or limitation.

## Zillow data to inspect or pull

2–3 active price-reduction candidates.

## Files to create or update

- `docs/zillow_field_notes.md`

## Inputs

Active listing addresses or URLs.

## Outputs

Success/failure results and missing fields.

## Acceptance criteria

- Tests at least 2–3 active listings.
- Documents whether active-listing detail calls are supported.
- Does not assume unavailable price history.

## Data-quality checks

- Detail call support status.
- Price history availability.
- Days on Zillow availability.
- Tax/sale history availability.
- Listing description availability.

## Correction / refinement step

If active detail calls fail, document the limitation and keep active MVP based on search-level fields only.

## Prompt text

```text
For each of the following active Zillow listings that appeared in a price-reduction search, test whether the Zillow detail tool can return full listing details.

Properties:
[PASTE 2–3 ACTIVE LISTING ADDRESSES OR URLS]

Try to retrieve:
- previous list price
- current list price
- price cut amount
- price cut date
- full price history
- days on Zillow
- listing description
- tax history
- sale history
- HOA fee
- property tax
- listing agent
- brokerage

If active listing details are not supported, say so clearly.

Do not infer missing fields.
Do not score price cuts.
Do not recommend properties.
```
