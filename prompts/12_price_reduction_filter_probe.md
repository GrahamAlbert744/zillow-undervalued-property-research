# Prompt 12 — Price-Reduction Filter Probe

## Phase

Phase 10B

## Purpose

Test whether Zillow can return a price-reduction-filtered universe.

## What to build

Document whether price reduction can be used as a search-source flag.

## Zillow data to inspect or pull

Active residential listings with price-reduction filter applied.

## Files to create or update

- `docs/zillow_field_notes.md`

## Inputs

Approximate 25-mile search region.

## Outputs

Search count and field availability for price-reduced listings.

## Acceptance criteria

- Confirms whether the price-reduction filter works.
- Confirms whether exact price cut amount/date are returned.
- Does not score price reductions yet.

## Data-quality checks

- Missing previous price.
- Missing price-cut amount.
- Missing price-cut date.
- Missing days on market.
- Active listing detail limitation.

## Correction / refinement step

If only the filter match is available, use `zillow_price_reduction_filter_match` as a weak flag, not a score metric.

## Prompt text

```text
Search Zillow for active residential properties near ZIP code 02131 within the approximate 25-mile research area, using a price-reduction filter if supported.

Include:
- single-family homes
- condos
- townhomes
- multifamily homes

Listing statuses:
- for sale by agent
- for sale by owner
- coming soon, if supported
- new construction

Return up to 100 results.

For each property, return all available fields, especially:
- address
- city
- state
- ZIP code
- latitude
- longitude
- current listing price
- previous price, if available
- price cut amount, if available
- price cut percentage, if available
- price cut date, if available
- days on market, if available
- beds
- baths
- square feet
- property type
- Zillow URL

Do not score properties.
Do not recommend properties.
The goal is only to test whether price-reduction details are available.
```
