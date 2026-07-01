# Prompt 26 — Future Comparable-Sales Probe

## Phase

Future valuation/comps validation

## Purpose

Determine whether Zillow connector can support comparable-sale data.

## What to build

A comps availability audit.

## Zillow data to inspect or pull

One property at a time.

## Files to create or update

- future: `data/interim/comps_probe_results.csv`
- future: `src/comps.py`
- future: `docs/zillow_field_notes.md`

## Inputs

Subject property address or URL.

## Outputs

Comparable-sale field availability.

## Acceptance criteria

- Identifies whether comps are returned.
- Preserves source context.
- Does not estimate fair value yet.

## Data-quality checks

- comp address
- comp sale date
- comp sale price
- comp square feet
- comp distance
- same property type
- sale timing
- missing source URL

## Correction / refinement step

If comps are unstructured or incomplete, keep them as notes until parser is validated.

## Prompt text

```text
For this property, identify whether Zillow provides comparable sale or nearby sold-property information.

Property:
[PASTE ADDRESS OR URL]

Return available comparable-sale fields only if visible:
- comp address
- sale date
- sale price
- beds
- baths
- square feet
- property type
- distance from subject
- price per square foot
- source URL or reference

If comparable sales are not available from the connector, say so clearly.

Do not estimate fair value yet.
Do not recommend buying or selling.
The goal is only to test whether comparable-sale data is available.
```
