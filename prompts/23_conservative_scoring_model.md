# Prompt 23 — Build First Conservative Scoring Model

## Phase

After geography and data-quality validation

## Purpose

Create the first transparent MVP scoring model.

## What to build

A conservative score that ranks properties for research review only.

## Zillow data to inspect or pull

Use normalized active-listing dataframe and validated detail-probe fields if available.

## Files to create or update

- `src/scoring.py`
- `scripts/create_research_queue.py`
- `outputs/tables/undervaluation_scores.csv`
- `outputs/tables/top_25_property_research_queue.csv`
- `outputs/tables/excluded_properties.csv`
- `docs/scoring_methodology.md`

## Inputs

- `data/processed/all_properties_normalized.csv`
- data-quality flags
- optional detail-probe data

## Outputs

Scored research queue and excluded properties table.

## Acceptance criteria

- Applies hard filters.
- Uses only validated fields.
- Penalizes missing data.
- Produces a research queue, not buy/sell recommendations.
- Explains score components.

## Data-quality checks

- Exclude missing price.
- Exclude invalid square feet from price-per-square-foot metrics.
- Exclude outside-radius properties from main ranking.
- Penalize missing Zestimate/Rent Zestimate rather than making property appear attractive.
- Keep insufficient-data properties in review queue.

## Correction / refinement step

If detail fields are too sparse, use search-level scoring only and mark valuation confidence low.

## Prompt text

```text
Create the first conservative scoring model for the Zillow undervalued-property research project.

Goal:
Create a transparent research-ranking score, not an investment recommendation.

Create or update:
- src/scoring.py
- scripts/create_research_queue.py
- outputs/tables/undervaluation_scores.csv
- outputs/tables/top_25_property_research_queue.csv
- outputs/tables/excluded_properties.csv
- docs/scoring_methodology.md

Use a 100-point score:
- Valuation score: 40
- Income potential score: 20
- Market/location score: 15
- Property usefulness score: 15
- Data-quality/confidence score: 10

Hard filters:
- outside_target_radius is True
- missing or invalid price
- non-residential home type
- invalid square feet for calculations
- clearly insufficient core data

Soft signals:
- lower price_per_sqft relative to similar local properties
- price below Zestimate only if Zestimate is available and validated
- gross rent yield only if Rent Zestimate is available and validated
- complete core data
- valid geocode
- no duplicate warning

Rules:
- Do not recommend buying or selling.
- Label outputs as research candidates only.
- Missing data should reduce confidence.
- Do not let missing Zestimate create fake undervaluation.
```
