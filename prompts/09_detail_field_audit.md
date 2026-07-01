# Prompt 09 — Detail Field Audit

## Phase

Phase 9A

## Purpose

Audit detail/valuation fields after one or more property-detail calls.

## What to build

A detail-field availability table.

## Zillow data to inspect or pull

Detail-pull results from Prompt 08.

## Files to create or update

- `docs/zillow_field_notes.md`
- `docs/data_dictionary.md`
- `docs/scoring_methodology.md`

## Inputs

Zillow detail output.

## Outputs

Availability and trust classification.

## Acceptance criteria

- Separates returned values from missing values.
- Flags fields that require validation.
- Identifies fields safe only for context, not scoring.

## Data-quality checks

- Zestimate dependency on list price
- Rent Zestimate uncertainty
- Comps parsing reliability
- Missing sale/tax/history fields
- Active listing detail unsupported

## Correction / refinement step

If a field is available only for some property types, document property-type-specific availability.

## Prompt text

```text
Audit the Zillow detail output below for my real-estate research project.

Classify each field as:
1. Available and useful
2. Available but use cautiously
3. Available only as unstructured text
4. Missing from the detail output
5. Not safe for scoring without validation

Fields to audit:
- Zestimate
- Zestimate per square foot
- Zestimate range
- Rent Zestimate
- comparable homes
- comparable sale price
- comparable sale date/timing
- listing description
- days on Zillow
- price history
- tax history
- sale history
- year built
- HOA fee
- property tax
- lot size
- schools
- neighborhood
- listing agent
- brokerage
- listing status
- last updated date

Also state:
- whether the detail output changes the MVP scoring plan
- which fields should be added to the data dictionary
- which fields should be stored in a separate detail-probe table
- which fields remain unsafe for scoring

Detail output:
[PASTE OUTPUT HERE]
```
