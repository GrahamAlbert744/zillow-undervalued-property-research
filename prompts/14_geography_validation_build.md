# Prompt 14 — Build Geography Validation

## Phase

Phase 11 / 11B

## Purpose

Add true distance validation from ZIP `02131`.

## What to build

Haversine distance utilities and normalized dataframe fields.

## Zillow data to inspect or pull

Use normalized active-listing dataframe with latitude/longitude.

## Files to create or update

- `src/geocoding.py`
- `src/field_mapping.py`
- `src/data_quality.py`
- `docs/data_dictionary.md`

## Inputs

Latitude and longitude for each property.

## Outputs

- `distance_from_02131_miles`
- `outside_target_radius`
- optional geography review table

## Acceptance criteria

- Distance is calculated for records with valid lat/long.
- Missing lat/long remains missing.
- Outside-radius flag is true when distance > 25 miles.
- Pipeline does not crash on missing or invalid coordinates.

## Data-quality checks

- Missing lat/long.
- Bad geocode.
- Outside 25-mile target radius.
- Undisclosed address.
- Possible duplicate lat/long.

## Correction / refinement step

If NaN coordinates cause errors, make the function NaN-safe.

## Prompt text

```text
Add geography validation to the Zillow undervalued-property research project.

Create or update:
- src/geocoding.py
- src/field_mapping.py
- src/data_quality.py
- docs/data_dictionary.md

Goal:
Calculate distance from ZIP code 02131 and flag properties outside the 25-mile research radius.

Requirements:
- Use the haversine formula.
- Center coordinates should approximate ZIP 02131.
- Add distance_from_02131_miles to the normalized dataframe.
- Add outside_target_radius to the normalized dataframe.
- Add missing_lat_long and outside_target_radius to data-quality checks.
- Do not guess missing coordinates.
- Do not trust the Zillow search boundary by itself.
- Do not score properties yet.

Acceptance criteria:
- all_properties_normalized.csv includes distance_from_02131_miles and outside_target_radius.
- Missing coordinates do not crash the pipeline.
- Roslindale sample records show small distances.
```
