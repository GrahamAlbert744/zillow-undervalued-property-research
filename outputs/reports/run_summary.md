# Zillow Property Pipeline Run Summary

Run created: `2026-07-08 22:14:28`

## Purpose

Summarize the current Zillow property pipeline output. This report is for data validation and workflow tracking only. It does not recommend buying or selling any property.

## Input files

- Normalized properties: `data\processed\all_properties_normalized.csv`
- Data-quality flags: `outputs\tables\property_data_quality_flags.csv` (found)
- Missingness report: `outputs\tables\property_missingness_report.csv` (found)
- Property type summary: `outputs\tables\property_type_summary.csv` (found)

## Core counts

- Total normalized records: **10**
- Records needing review: **0**
- Records outside 25-mile radius: **0**
- Records missing latitude/longitude: **2**

## Core field availability

- Price values available: **10**
- Square-foot values available: **10**
- Zestimate values available: **0**
- Rent Zestimate values available: **0**
- Distance-from-02131 values available: **9**

## Median metrics

- Median listing price: **705000.0**
- Median square feet: **1603.0**
- Median price per sqft: **441.87**
- Median distance from 02131: **0.35 miles**

## Property type counts

| Home type | Count |
|---|---:|
| condo | 4 |
| single_family | 3 |
| multi_family | 2 |
| townhome | 1 |


## Missingness summary

| Field | Missing count |
|---|---:|
| `address` | 0 |
| `price` | 0 |
| `beds` | 0 |
| `baths` | 0 |
| `square_feet` | 0 |
| `home_type` | 0 |
| `latitude` | 1 |
| `longitude` | 1 |
| `zestimate` | 10 |
| `rent_zestimate` | 10 |
| `distance_from_02131_miles` | 1 |


## Important interpretation notes

- This pipeline is still pre-scoring.
- Distance validation is now part of the normalized property file if `src/geocoding.py` is available.
- Missing fields should be flagged, not guessed.
- `data_needs_review` may come from the data-quality file rather than the normalized file.
- Properties outside the 25-mile radius should be excluded from future main rankings.

## Next recommended step

Confirm that `distance_from_02131_miles` and `outside_target_radius` are present in `all_properties_normalized.csv`, then update `docs/data_dictionary.md` if needed.
