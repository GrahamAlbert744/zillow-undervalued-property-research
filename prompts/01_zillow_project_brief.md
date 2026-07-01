# Prompt 01 — Zillow Project Brief and Plan Redesign

## Phase

Project planning / Phase 1

## Purpose

Ask the Zillow connector and ChatGPT to challenge the project plan based on actual field availability.

## What to build

A revised project plan that reflects what Zillow can realistically provide.

## Zillow data to inspect or pull

No pull required yet. This is a planning prompt.

## Files to create or update

- `docs/project_plan.md`
- `docs/data_dictionary.md`
- `docs/scoring_methodology.md`
- `docs/zillow_field_notes.md`
- `docs/decision_log.md`

## Inputs

The full project idea and desired fields.

## Outputs

A revised overview, architecture, database design, scoring model, roadmap, prompt library, risks, and open questions.

## Acceptance criteria

- Clearly separates MVP fields from future fields.
- Does not assume unavailable Zillow fields exist.
- Keeps the project framed as a research queue, not investment advice.
- Recommends a phased build sequence.

## Data-quality checks

- Identify missing, stale, unreliable, or validation-required fields.
- Identify duplicate risks.
- Identify geocoding and radius-validation risks.

## Correction / refinement step

If Zillow fields are not actually available, revise the schema and scoring model instead of forcing missing fields.

## Prompt text

```text
I am starting a long-term data science project using the Zillow connector, Python, GitHub, Jupyter Lab, and ChatGPT.

Project purpose:
I want to build a high-quality real estate research system that helps me identify potentially undervalued residential properties within 25 miles of ZIP code 02131.

The goal is not to make automatic buy/sell decisions. The goal is to create a structured research workflow that helps me collect property data, clean it, score opportunities, flag risks, and create a ranked research queue for human review.

Search area:
- Center ZIP code: 02131
- Radius: 25 miles
- Primary market: Greater Boston / eastern Massachusetts
- Property types to consider:
  - single-family homes
  - condos
  - townhomes
  - multifamily properties if available
- Exclude:
  - clearly distressed or uninhabitable properties unless explicitly flagged for separate review
  - properties with missing core valuation data unless they are kept in a needs-research queue

Use the Zillow connector’s actual data structure to redesign and improve this project plan.

Please return:
1. Revised project overview
2. Revised architecture
3. Revised database design
4. Revised scoring model
5. Revised phased roadmap
6. New prompt library
7. List of risks and limitations
8. List of questions I should answer before implementation

Important:
Do not recommend buying or selling.
Do not make legal, tax, mortgage, or investment recommendations.
Do not hallucinate missing property facts.
If a field is unavailable, flag it.
```
