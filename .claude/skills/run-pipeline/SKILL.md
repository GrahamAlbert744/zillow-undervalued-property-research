---
name: run-pipeline
description: This skill should be used when the user asks to "run the pipeline", "re-run the MVP pipeline", "regenerate the research queue", "refresh the pipeline outputs", "run all the scripts", or wants to confirm the anti-overclaim safeguards still hold after a data or code change.
---

# Run the Zillow Research Pipeline

Run the full conservative MVP pipeline for this project end-to-end, in the
fixed order described in `README.md` and `docs/decision_log.md` Decision
015, then report whether the anti-overclaim safeguards still hold.

## When to use this skill

Use it whenever raw Zillow data, a normalization/scoring script, or a
data-quality rule changes and the downstream tables need to be
regenerated — or simply to confirm the pipeline still runs cleanly.

Do not use it to add a new pipeline stage or change scoring logic; it only
re-runs the existing stages in order.

## Pipeline order

Run these from the project root, in this exact order — each stage reads the
previous stage's output:

```bash
python scripts/build_property_database.py
python scripts/run_data_quality_check.py
python scripts/create_active_listing_candidate_table.py
python scripts/create_valuation_context_features.py
python scripts/create_research_queue_table.py
python scripts/create_candidate_exclusion_review_table.py
python scripts/create_property_research_notes.py
python scripts/create_mvp_run_summary.py
```

`scripts/create_zillow_raw_sample.py` is a separate, manual dev step for
building `data/raw/zillow_raw_search_YYYYMMDD.json` from a fresh Zillow
connector pull — it is not part of this automatic re-run. Only run it if the
user explicitly wants to regenerate the raw sample from new connector output.

If any stage fails with a missing-input error, stop and report which stage
failed and why (each script raises `FileNotFoundError` naming the exact
input path it expected) — do not skip stages or invent workarounds.

## After running: report the safeguards

Read `outputs/reports/mvp_run_summary.md` (rewritten by the last step) and
report back:

1. **Anti-Overclaim Safeguards section** — all four counts (final scores,
   investment recommendations, buy/sell recommendations,
   backtesting-ready) must read `0`. If any is nonzero, treat this as a
   serious regression and flag it clearly — it means something in the
   pipeline started producing exactly the kind of output this project's
   guardrails (see `CLAUDE.md`) forbid.
2. **Data Quality / Research Queue / Exclusion counts** — summarize how many
   records ended up in each bucket, so the user can see at a glance whether
   the run looks like previous runs or changed materially.
3. Whether `outputs/property_research_notes/*.md` regenerated without a
   `ValueError` from the forbidden-language check in
   `scripts/create_property_research_notes.py` (a raised error there means a
   note would have contained buy/sell/investment language and was not
   written — surface this immediately rather than treating it as routine
   script noise).

## Why this exists as a skill, not a slash command

This is a multi-step, deterministic procedure with a fixed script order and
a fixed set of inputs/outputs — exactly the kind of repeatable workflow a
skill is for. It differs from a slash command in that Claude can decide to
invoke it on its own when the situation calls for it (e.g. "I changed the
data-quality thresholds, let me re-run the pipeline to check"), not only
when the user explicitly types a command.
