# Project Instructions — Zillow Undervalued Property Research

## What this project is

A conservative real-estate **research** workflow for residential properties
within 25 miles of ZIP code 02131 (Greater Boston / eastern Massachusetts).
It collects Zillow connector data, normalizes it, flags data-quality issues,
and produces a ranked **research queue for human review**. See `README.md`,
`docs/project_plan.md`, and `docs/decision_log.md` for full history.

It is explicitly **not** an automated buy/sell/investment decision engine.

## Guardrails (do not violate)

- **No buy/sell/investment-recommendation language anywhere**, including
  inside negated disclaimers ("not a buy recommendation" still contains the
  forbidden word). See the forbidden-phrase regex already enforced in
  `scripts/create_property_research_notes.py` as prior art — reuse that
  pattern rather than inventing a new check.
- Allowed output labels are limited to: `research first`, `watchlist`,
  `avoid`, `possible candidate after human review`, `needs data review`.
  Do not introduce labels like "buy", "strong buy", or "safe investment"
  (Decision 003).
- Missing or unreliable data must be **flagged, never guessed**, and must
  never make a property look more attractive (Decision 005).
- Respect the pipeline stage order already built:
  `normalize -> data-quality gates -> candidate gating -> valuation/context
  features -> research queue -> exclusion/hold review -> research notes`.
  Do not start scoring, status/lifecycle tracking, or backtesting until the
  upstream stages are validated on real data (Decisions 004, 007, 013).
- Record any major project decision in `docs/decision_log.md`, following its
  existing format (date / decision / reason / alternatives considered /
  implications / follow-up actions).

## Required workflow for substantive changes

"Substantive" = changes to code, scripts, `src/` modules, pipeline
behavior/logic, or docs that encode a project decision (README, project
plan, decision log, scoring/data-quality methodology).

For substantive changes:
1. **Always enter plan mode first.**
2. **Always ask clarifying questions** before finalizing the plan whenever
   intent, scope, or approach is ambiguous — don't assume.
3. Write the plan and get it approved before editing or running anything
   that changes repo state.

**Exempt from this** (may proceed directly, no plan mode required):
read-only exploration/audits, running existing scripts to inspect output,
answering questions about the repo, and typo/formatting-only doc fixes that
don't change meaning.
