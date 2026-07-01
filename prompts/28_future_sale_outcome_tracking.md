# Prompt 28 — Future Sale Outcome Tracking

## Phase

Future sale-outcome tracking

## Purpose

Capture final sale prices and compare them to frozen model estimates.

## What to build

Sale outcome tracker and model evaluation inputs.

## Zillow data to inspect or pull

Confirmed sold outcomes only.

## Files to create or update

- `src/outcome_tracker.py`
- `src/model_evaluation.py`
- `outputs/tables/sale_outcomes.csv`
- `outputs/reports/model_accuracy_report.md`
- `tests/test_outcome_tracker.py`

## Inputs

Sold properties with confirmed sale date and final sale price.

## Outputs

Sale outcome records and prediction-error metrics.

## Acceptance criteria

- Calculates prediction error only when final sale price exists.
- Preserves model version used at prediction time.
- Does not retroactively change old predictions.
- Leaves missing sale prices in pending-outcome queue.

## Data-quality checks

- final sale price confirmed
- sale date confirmed
- original list price exists
- last list price exists
- model version exists
- valuation snapshot predates sale

## Correction / refinement step

If confirmed sale price is missing, do not calculate error.

## Prompt text

```text
Create sale outcome tracking for the Zillow undervalued-property research project.

Goal:
When a property eventually sells, capture the final sale price and compare it to the model’s estimated fair value from before the sale.

Create or update:
- src/outcome_tracker.py
- src/model_evaluation.py
- outputs/tables/sale_outcomes.csv
- outputs/reports/model_accuracy_report.md
- tests/test_outcome_tracker.py

For each sold property, calculate:
- original_list_price
- last_list_price_before_contract
- final_sale_price
- sale_date
- estimated_fair_value_at_time_of_prediction
- sale_price_minus_estimated_fair_value
- sale_price_vs_estimated_fair_value_pct
- sale_price_vs_original_list_pct
- sale_price_vs_last_list_pct
- absolute_prediction_error
- absolute_prediction_error_pct
- model_bias_direction

Rules:
- Use only confirmed sale prices.
- Do not treat list price, pending price, Zestimate, or asking price as final sale price.
- If sale price is missing, keep the property in pending_outcome_queue.
- Preserve the model version used at the time of the estimate.
- Do not retroactively change old predictions after the sale.
```
