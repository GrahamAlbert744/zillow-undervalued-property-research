# Prompt 03 — Search-Level Field Audit

## Phase

Phase 9 / Phase 10

## Purpose

Compare Zillow connector output against the desired project schema.

## What to build

A field audit classifying fields by usability.

## Zillow data to inspect or pull

Use output from Prompt 02 or any later search pull.

## Files to create or update

- `docs/zillow_field_notes.md`
- `docs/data_dictionary.md`
- `docs/decision_log.md`

## Inputs

Raw Zillow connector search output.

## Outputs

A field audit table.

## Acceptance criteria

- Classifies each desired field as available, cautious, missing, detail-required, or not safe.
- Identifies duplicate and stale-data risks.
- Recommends MVP-safe fields.

## Data-quality checks

- Missing price
- Missing square feet
- Missing lat/long
- Duplicate address
- Duplicate lat/long
- Undisclosed address
- Missing Zestimate/rent estimate
- Ambiguous status fields

## Correction / refinement step

Revise the data dictionary and scoring methodology based on actual field availability.

## Prompt text

```text
Review the Zillow connector output pasted below.

Task:
Create a field audit for my Zillow undervalued-property research project.

For each field, classify it as:
1. Available and safe for MVP
2. Available but requires caution
3. Missing from search-level output
4. Requires property-detail pull
5. Not reliable enough for scoring yet

Fields to audit:
- zpid
- address
- city
- state
- zip_code
- latitude
- longitude
- listing status
- price
- beds
- baths
- square feet
- lot size
- home type
- Zestimate
- Rent Zestimate
- days on market
- price history
- tax history
- sale history
- listing description
- HOA fee
- property tax
- Zillow URL

Also identify:
- duplicate risks
- stale listing risks
- missing-data risks
- fields that should not be used for scoring yet

Connector output:
[PASTE OUTPUT HERE]
```
