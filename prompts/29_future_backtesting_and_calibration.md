# Prompt 29 — Future Model Backtesting and Calibration

## Phase

Future model evaluation

## Purpose

Evaluate scoring/fair-value model accuracy after enough confirmed sale outcomes exist.

## What to build

Backtesting and calibration module.

## Zillow data to inspect or pull

Confirmed sale outcomes and frozen valuation snapshots.

## Files to create or update

- `src/model_evaluation.py`
- `src/scoring.py`
- `docs/model_backtesting.md`
- `outputs/reports/model_accuracy_report.md`
- `outputs/tables/model_evaluation_summary.csv`

## Inputs

- `sale_outcomes.csv`
- valuation snapshots
- model versions

## Outputs

Model accuracy report.

## Acceptance criteria

- Reports error and bias.
- Separates recommendations from automatic changes.
- Does not recalibrate with too few outcomes.
- Preserves model versions.

## Data-quality checks

- enough sold outcomes
- no leakage
- model estimate predates sale
- sale price confirmed
- model version stored

## Correction / refinement step

Do not change thresholds based on fewer than 20 sold outcomes.

## Prompt text

```text
Create a model backtesting and calibration module.

Goal:
Use closed-sale outcomes to evaluate whether the fair value model is accurate and whether scoring rules should be adjusted.

Create or update:
- src/model_evaluation.py
- src/scoring.py
- docs/model_backtesting.md
- outputs/reports/model_accuracy_report.md
- outputs/tables/model_evaluation_summary.csv

Evaluate:
- mean absolute error percentage
- median absolute error percentage
- mean bias percentage
- percent of predictions within 5%
- percent within 10%
- percent within 15%
- performance by property type
- performance by city
- performance by price band
- performance by data-quality tier
- performance by score bucket

Calibration rules:
- Do not update scoring thresholds based on fewer than 20 sold outcomes.
- Treat 20–50 sales as exploratory.
- Treat 50+ sales as enough to consider minor threshold updates.
- Preserve old model versions.
- Create a new model_version whenever scoring logic changes.

No model changes should be applied without a written model-change note.
```
