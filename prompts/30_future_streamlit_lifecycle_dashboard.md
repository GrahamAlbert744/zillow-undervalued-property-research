# Prompt 30 — Future Streamlit Lifecycle Dashboard

## Phase

Future dashboarding

## Purpose

Create a dashboard for active rankings, status tracking, sold outcomes, and model accuracy.

## What to build

Streamlit dashboard pages.

## Zillow data to inspect or pull

Uses local tables, not direct connector calls.

## Files to create or update

- future: `app.py`
- future: `src/dashboard_helpers.py`
- future: dashboard documentation

## Inputs

- active research queue
- status history
- sale outcomes
- model evaluation summaries

## Outputs

Interactive dashboard.

## Acceptance criteria

- Allows filtering by status.
- Allows export to CSV.
- Shows data-quality flags.
- Clearly labels results as research-only.

## Data-quality checks

- missing score
- missing status
- stale data
- missing sale outcomes
- uncertain final sale price

## Correction / refinement step

If lifecycle tables are missing, dashboard should show a clear unavailable message rather than crashing.

## Prompt text

```text
Update the Streamlit dashboard to include property lifecycle and model accuracy tracking.

Add dashboard pages:
1. Overview
2. Ranked Active Properties
3. Property Detail
4. Map View
5. Watchlist
6. Status Tracker
7. Sold Outcomes
8. Model Accuracy
9. Model Version History
10. Data Quality

Status Tracker page:
Show:
- address
- current status
- prior status
- first seen date
- last seen date
- original list price
- current list price
- price change
- estimated fair value
- total score
- watchlist status
- next action

Sold Outcomes page:
Show:
- address
- original list price
- final sale price
- estimated fair value
- sale price vs fair value
- prediction error percentage
- sale date
- model version
- accuracy band

Rules:
- Dashboard must not recommend buying or selling.
- Missing data should be clearly labeled.
- User should be able to export tables to CSV.
```
