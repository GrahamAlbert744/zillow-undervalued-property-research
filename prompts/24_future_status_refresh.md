# Prompt 24 — Future Weekly Active Status Refresh

## Phase

Future lifecycle tracking

## Purpose

Check whether tracked active properties remain active, go pending, sell, or disappear.

## What to build

A future refresh prompt and eventual status-tracking process.

## Zillow data to inspect or pull

List of tracked property addresses/URLs.

## Files to create or update

- future: `outputs/tables/status_changes.csv`
- future: `outputs/reports/weekly_summary.md`
- future: `src/status_tracker.py`

## Inputs

Tracked property list.

## Outputs

Current status and price-change observations.

## Acceptance criteria

- Does not assume missing/off-market equals sold.
- Flags unclear statuses.
- Captures confirmed sale price only when explicitly available.

## Data-quality checks

- status ambiguous
- status changed
- price changed
- property removed
- sale price missing
- URL unavailable

## Correction / refinement step

If status is unclear, mark `needs_manual_review`.

## Prompt text

```text
Check the current Zillow status for the following properties.

For each property, return:
- address
- Zillow URL
- current listing status
- current list price
- whether it appears active
- whether it appears pending, contingent, under contract, sold, off market, or removed
- any visible status text
- any visible price change
- any visible sale price, only if confirmed

Important:
Do not assume a property sold just because it is missing or off market.
If status is unclear, mark it as needs manual review.

Properties:
[PASTE PROPERTY LIST WITH URLS]
```
