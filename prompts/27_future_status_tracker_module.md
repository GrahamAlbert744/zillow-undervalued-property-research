# Prompt 27 — Future Status Tracker Module

## Phase

Future lifecycle tracking

## Purpose

Create a property status tracking module after the active-listing pipeline and first score are stable.

## What to build

Status history, valuation snapshots, sale outcomes, and model evaluation schema.

## Zillow data to inspect or pull

Weekly/current status refresh data.

## Files to create or update

- `src/status_tracker.py`
- `src/database.py`
- `tests/test_status_tracker.py`
- `docs/status_tracking_methodology.md`

## Inputs

Prior and current property snapshots.

## Outputs

Status history and change detection.

## Acceptance criteria

- Same property can have multiple status records.
- Detects status changes.
- Preserves historical valuations.
- Flags ambiguous statuses.

## Data-quality checks

- missing status
- ambiguous status
- disappeared listing
- status conflict
- price change
- duplicate ZPID/address

## Correction / refinement step

If a property disappears from active search results, mark as `removed` or `needs_manual_review`, not sold.

## Prompt text

```text
Create a property status tracking module for the Zillow undervalued-property research project.

Goal:
Track each property over time from active listing to under contract, pending, sold, off market, or unknown.

Create or update:
- src/status_tracker.py
- src/database.py
- tests/test_status_tracker.py
- docs/status_tracking_methodology.md

Database tables to add:
1. property_status_history
2. valuation_snapshots
3. sale_outcomes
4. model_evaluation

Status categories:
- for_sale
- price_reduced
- price_increased
- under_contract
- pending
- contingent
- sold
- off_market
- removed
- unknown
- needs_manual_review

Requirements:
- Store a status snapshot every time the pipeline runs.
- Keep original list price.
- Keep most recent list price.
- Keep status text from Zillow.
- Normalize status category.
- Detect status changes since prior run.
- Preserve fair value estimate that existed before status changed.
- Do not overwrite historical model estimates.
- If a property disappears from active search results, mark it as removed or needs_manual_review rather than assuming it sold.
```
