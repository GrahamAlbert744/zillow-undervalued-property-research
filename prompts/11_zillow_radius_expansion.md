# Prompt 11 — 25-Mile Radius Expansion

## Phase

Phase 10A

## Purpose

Expand search beyond ZIP `02131` while still requiring Python distance validation.

## What to build

No immediate local code. Capture search universe and field availability.

## Zillow data to inspect or pull

Active listings in approximate 25-mile region around `02131`.

## Files to create or update

- `docs/zillow_field_notes.md`
- later: raw search file
- later: normalized table

## Inputs

Approximate 25-mile polygon or regional search specification.

## Outputs

Search result count and sample active listing records.

## Acceptance criteria

- Search returns residential listings across the broader region.
- Latitude and longitude are returned for distance validation.
- Does not assume connector boundary equals true radius.

## Data-quality checks

- Property outside target radius.
- Missing lat/long.
- Duplicate records.
- Mixed property types.
- New construction plans vs individual listings.

## Correction / refinement step

Use Python haversine distance to validate actual 25-mile inclusion.

## Prompt text

```text
Search for active residential properties within the Greater Boston / eastern Massachusetts area near ZIP code 02131.

Target:
- properties that may be within roughly 25 miles of ZIP code 02131

Include:
- single-family homes
- condos
- townhomes
- multifamily homes

Return up to 50–100 properties.

For each property, include:
- address
- city
- state
- ZIP code
- latitude
- longitude
- price
- beds
- baths
- square feet
- property type
- lot size
- listing status
- Zillow URL

Important:
Do not assume the property is within 25 miles just because it appears in the search.
Return latitude and longitude whenever available so I can calculate distance manually in Python.

Do not score properties.
Do not recommend properties.
This is a data-collection and geography-validation pull only.
```
