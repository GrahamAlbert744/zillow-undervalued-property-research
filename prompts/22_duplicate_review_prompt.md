# Prompt 22 — Duplicate Review Prompt

## Phase

After normalization / before scoring

## Purpose

Review suspected duplicate Zillow records conservatively.

## What to build

A manual duplicate-review decision table.

## Zillow data to inspect or pull

Rows flagged by duplicate address or duplicate lat/long.

## Files to create or update

- `outputs/tables/properties_needing_review.csv`
- `docs/decision_log.md`
- later: `outputs/tables/duplicate_review.csv`

## Inputs

Suspected duplicate rows.

## Outputs

Duplicate classification and conservative deduplication recommendation.

## Acceptance criteria

- Preserves separate condo units.
- Preserves separate multifamily/unit records when ambiguous.
- Does not auto-delete uncertain records.
- Flags true duplicates.

## Data-quality checks

- same ZPID
- same address
- same lat/long
- same price/sqft/beds/baths
- different unit numbers
- new construction plan vs actual unit
- multifamily vs unit listing

## Correction / refinement step

If duplicate status is ambiguous, keep both and flag for manual review.

## Prompt text

```text
Review the following suspected duplicate Zillow records.

Task:
Identify whether these appear to be:
1. True duplicate listings
2. Separate units in the same building
3. Same property with different Zillow IDs
4. New construction plans
5. Ambiguous and needing manual review

For each cluster, recommend a conservative deduplication rule.

Rules:
- Do not delete records automatically unless the duplicate is obvious.
- Preserve separate condo units.
- Preserve separate multifamily and unit listings if they may represent different legal properties.
- Flag ambiguous records for manual review.

Suspected duplicate records:
[PASTE ROWS HERE]
```
