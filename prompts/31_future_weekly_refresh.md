# Prompt 31 — Future Weekly Refresh with Status and Sale-Price Tracking

## Phase

Future automation / recurring workflow

## Purpose

Refresh listings, detect status changes, update outcomes, and generate weekly report.

## What to build

Weekly refresh pipeline.

## Zillow data to inspect or pull

Current active listing search and tracked property status checks.

## Files to create or update

- `outputs/reports/weekly_summary.md`
- `outputs/tables/new_listings.csv`
- `outputs/tables/price_changes.csv`
- `outputs/tables/status_changes.csv`
- `outputs/tables/new_sold_outcomes.csv`
- `outputs/tables/pending_outcome_queue.csv`
- `outputs/reports/model_accuracy_report.md`

## Inputs

Prior snapshot and current Zillow search/status results.

## Outputs

Weekly summary and change tables.

## Acceptance criteria

- Does not confuse under contract with sold.
- Does not invent sale prices.
- Status changes are auditable.
- Sale outcomes are connected to frozen model version.

## Data-quality checks

- listing disappeared
- ambiguous status
- sale price missing
- duplicate property
- changed ZPID
- missing URL
- missing model version

## Correction / refinement step

If status or sale outcome is unclear, route to manual review.

## Prompt text

```text
Update the weekly refresh process for the Zillow undervalued-property research project.

Goal:
Every weekly run should refresh listings, detect status changes, and update model outcome tracking.

Pipeline steps:
1. Pull current Zillow search results.
2. Normalize the new listing data.
3. Match current listings to existing properties by zpid, address, and lat/long.
4. Detect new listings.
5. Detect active listings still for sale.
6. Detect price changes.
7. Detect under-contract or pending status.
8. Detect sold status if available.
9. Capture final sale price only if confirmed.
10. Move properties with missing sale prices into pending_outcome_queue.
11. Update status_history.
12. Update sale_outcomes.
13. Recalculate active-property scores.
14. Evaluate model accuracy for newly sold properties.
15. Generate weekly summary.

Weekly summary sections:
- New high-scoring properties
- Major price cuts
- Properties newly under contract
- Properties newly sold
- Sale outcomes added
- Prediction errors
- Model accuracy changes
- Properties needing manual status review
- Recommended next actions

Rules:
- Do not confuse under contract with sold.
- Do not invent sale prices.
- Do not overwrite historical model estimates.
```
