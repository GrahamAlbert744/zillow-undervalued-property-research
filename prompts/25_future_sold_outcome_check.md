# Prompt 25 — Future Sold Outcome Check

## Phase

Future sale-outcome tracking

## Purpose

Check whether tracked properties have confirmed final sale outcomes.

## What to build

A future sold-outcome collection prompt.

## Zillow data to inspect or pull

Tracked properties that are pending, sold, off-market, or removed.

## Files to create or update

- future: `outputs/tables/sale_outcomes.csv`
- future: `outputs/tables/pending_outcome_queue.csv`

## Inputs

Tracked property list.

## Outputs

Confirmed sale outcomes or pending-outcome flags.

## Acceptance criteria

- Uses only confirmed sale prices.
- Does not treat Zestimate or list price as sale price.
- Records uncertainty.

## Data-quality checks

- sale date exists
- final sale price exists
- sale price is confirmed
- last visible list price available
- original list price available

## Correction / refinement step

If final sale price is unavailable, mark `pending_outcome`.

## Prompt text

```text
For the following properties, check whether each has a confirmed sold outcome.

For each property, return:
- address
- Zillow URL
- current status
- sale date, if confirmed
- final sale price, if confirmed
- last visible list price, if available
- whether the sale price is confirmed or merely estimated
- any uncertainty or missing data

Rules:
- Do not treat Zestimate as sale price.
- Do not treat list price as sale price.
- Do not invent sale prices.
- If final sale price is unavailable, mark the property as pending_outcome.

Properties:
[PASTE PROPERTY LIST]
```
