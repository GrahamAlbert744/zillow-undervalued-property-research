# Prompt 04 — Create Local Raw Sample Script

## Phase

Phase 9

## Purpose

Turn the first Zillow connector observations into a local raw JSON development sample.

## What to build

A script that writes a small raw Zillow JSON sample to `data/raw/`.

## Zillow data to inspect or pull

Use selected records from the initial 02131 connector pull.

## Files to create or update

- `scripts/create_zillow_raw_sample.py`
- `data/raw/zillow_raw_search_YYYYMMDD.json`

## Inputs

Manual observations from the Zillow connector search.

## Outputs

A local raw JSON file.

## Acceptance criteria

- Script runs without crashing.
- Raw JSON file is created.
- Record count prints.
- No credentials or API tokens are written.
- File structure supports later normalization.

## Data-quality checks

- Confirm key fields exist in at least several rows.
- Include at least one missing/edge-case row if observed, such as undisclosed address.
- Preserve raw values without premature cleaning.

## Correction / refinement step

If later connector output has a different structure, update the raw sample and field mapping.

## Prompt text

```text
Create a Python script for my Zillow undervalued-property research project that writes a small local raw Zillow JSON sample.

The script should:
- be named scripts/create_zillow_raw_sample.py
- create data/raw/ if needed
- write data/raw/zillow_raw_search_YYYYMMDD.json
- include metadata such as source, search area, search date, and notes
- include 10–25 representative Zillow records from the connector output
- preserve fields such as zpid, address, city, state, zip_code, latitude, longitude, status, home_type, price, beds, baths, square_feet, zestimate if available, rent_zestimate if available, and zillow_url
- print the output path and record count

Do not include credentials.
Do not build scoring.
Do not modify processed outputs yet.
```
