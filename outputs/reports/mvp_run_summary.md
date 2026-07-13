# Zillow MVP Pipeline Run Summary

Run created: `2026-07-12 21:18:44`

## Purpose

Roll up the full conservative MVP pipeline: normalization, data-quality gates, candidate gating, valuation/context features, research queue, exclusion/hold review, and property research notes. This report is for workflow tracking only. It does not recommend buying or selling any property.

## Input files

- `data\processed\all_properties_normalized.csv` (found)
- `outputs\tables\active_listing_candidate_summary.csv` (found)
- `outputs\tables\valuation_context_feature_summary.csv` (found)
- `outputs\tables\property_research_queue_summary.csv` (found)
- `outputs\tables\candidate_exclusion_review_summary.csv` (found)
- `outputs\tables\property_research_notes_summary.csv` (found)

## Data Quality

- Total normalized active-listing records pulled: **10**
- Rankable-later candidates: **9**
- Needs-review candidates: **1**
- Held candidates: **0**
- Rejected candidates: **0**
- Missing latitude/longitude: **1**
- Undisclosed addresses: **1**

## Valuation Context

- Properties with price-per-sqft context: **9**
- Properties with Zestimate context: **0**
- Properties with Rent Zestimate / income context: **0**
- Properties far below home-type median price per sqft: **2**

Reminder: these are context signals, not a valuation score.
- Valuation score created: **0**

## Research Queue

- review_first: **2**
- review_next: **0**
- review_if_time: **6**
- watchlist_limited_data: **1**
- data_quality_review: **1**
- excluded: **0**

## Exclusion / Hold Review

- Properties preserved in the exclusion/hold review table: **1**
- Reject: **0**
- Hold: **0**
- Needs review: **1**

No excluded or held property was silently dropped from the pipeline.

## Property Research Notes

- Notes generated: **10**
- Notes with forbidden buy/sell language detected: **0**

## Anti-Overclaim Safeguards

- Final scores created: **0**
- Investment recommendations created: **0**
- Buy/sell recommendations created: **0**
- Records backtesting-ready: **0**

All four counts above should read 0 for this pipeline to remain MVP-safe.

## Limitations

- Active-listing detail pulls are not depended on for this pipeline; days on market, price history, tax history, HOA fee, and listing description remain unavailable for every record.
- Recently sold search prices are not confirmed final sale prices and are not used for backtesting.
- Zestimate and Rent Zestimate are context signals, not an appraisal or confirmed market rent.
- No scoring model, ranking, or buy/sell recommendation has been built yet. This report only summarizes the conservative research pipeline described in the project instructions.
