# Prompt 15 — Recently Sold Search / Sale Outcome Probe

## Phase

Phase 12A

## Purpose

Test whether Zillow can return a recently sold universe.

## What to build

Documentation of recently sold search field availability.

## Zillow data to inspect or pull

Recently sold residential properties in approximate 25-mile `02131` universe.

## Files to create or update

- `docs/zillow_field_notes.md`

## Inputs

Approximate 25-mile search region and recently sold status filter.

## Outputs

Recently sold search result count and fields.

## Acceptance criteria

- Confirms whether recently sold search works.
- Identifies whether sale date and final sale price are returned.
- Does not backtest.

## Data-quality checks

- Does returned price represent final sale price?
- Is sale date available?
- Are original list price, last list price, DOM, and price history available?
- Are statuses consistent?

## Correction / refinement step

If sale outcomes are not fully validated, create `sale_outcome_needs_validation = True`.

## Prompt text

```text
Search Zillow for recently sold residential properties within the approximate 25-mile research area around ZIP code 02131.

Include:
- single-family homes
- condos
- townhomes
- multifamily homes

Return up to 100 results.

For each result, return all available fields, especially:
- zpid
- address
- city
- state
- ZIP code
- latitude
- longitude
- property type
- beds
- baths
- square feet
- sold/search price
- status type
- status text
- sale date, if available
- final sale price confirmation, if available
- original list price, if available
- last list price before sale, if available
- days on market, if available
- Zillow URL

Do not backtest.
Do not assume search price is confirmed sale price unless Zillow clearly says it is.
```
