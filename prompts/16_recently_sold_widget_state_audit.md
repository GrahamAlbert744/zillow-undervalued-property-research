# Prompt 16 — Recently Sold Widget-State Audit

## Phase

Phase 12B

## Purpose

Audit enhanced widget-state fields for recently sold results.

## What to build

Documentation of additional fields exposed in widget state.

## Zillow data to inspect or pull

Recently sold widget-state result objects.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: `data/interim/recently_sold_probe_results.csv`

## Inputs

Recently sold search output including widget-state fields.

## Outputs

Field availability and status consistency audit.

## Acceptance criteria

- Identifies `zpid`, `statusType`, `statusText`, `price`, `priceLabel`, nested home status, zestimate, and rent Zestimate when present.
- Flags inconsistent statuses.
- Does not treat widget price as confirmed sale price without validation.

## Data-quality checks

- `statusType` vs `hdpData.homeInfo.homeStatus`
- missing zestimate
- missing rentZestimate
- display price vs numeric price
- duplicated addresses

## Correction / refinement step

If statuses conflict, add `status_conflict_flag`.

## Prompt text

```text
Audit the enhanced Zillow widget-state fields from the recently sold search results below.

For each field, identify:
- whether it appears
- whether it is consistently populated
- whether it is safe for future lifecycle tracking
- whether it requires validation before backtesting

Fields to inspect:
- zpid
- statusType
- statusText
- price
- priceLabel
- countryCurrency
- address
- beds
- baths
- area
- latLong.latitude
- latLong.longitude
- hdpData.homeInfo.homeStatus
- hdpData.homeInfo.homeType
- hdpData.homeInfo.zestimate
- hdpData.homeInfo.rentZestimate
- buildingName
- lotId

Also identify status conflicts, especially cases where top-level status says SOLD but nested homeStatus says FOR_SALE or another status.

Do not build backtesting.
Do not assume sale price is confirmed.
Widget-state output:
[PASTE OUTPUT HERE]
```
