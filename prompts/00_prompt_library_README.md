# Zillow Undervalued Property Research — Prompt Library

## Purpose

This folder stores reusable prompts for the Zillow undervalued-property research project.

Project goal: build a conservative real-estate research workflow for residential properties within 25 miles of ZIP code `02131`.

The system should:
- collect Zillow connector data
- normalize records
- flag data-quality issues
- build a research queue for human review
- avoid automatic buy/sell recommendations
- avoid legal, tax, mortgage, or investment advice
- flag missing fields instead of hallucinating them

## How to use these prompts

Use the prompts in order. Do not skip ahead to scoring, lifecycle tracking, or backtesting until the local data pipeline is stable.

Recommended order:

1. Planning and data availability
2. Active listing search-level pipeline
3. Detail-field probes
4. Geography validation
5. Price-reduction and recently-sold probes
6. Recently-sold enrichment table
7. Duplicate review
8. Conservative scoring
9. Status tracking
10. Sale-outcome tracking
11. Backtesting and dashboarding

## Storage location

Save this folder inside the project repo:

```text
zillow-undervalued-property-research/
  prompts/
```

## Safety rule

All outputs are research aids only. Do not recommend buying or selling. Do not invent property facts. If a field is unavailable, mark it unavailable or needing validation.
