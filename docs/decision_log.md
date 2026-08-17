\# Decision Log



\## Purpose



This document records important project decisions for the Zillow Undervalued Property Research project.



The goal is to make the project auditable, reproducible, and easier to restart after breaks.



Each major decision should include:



\- date

\- decision

\- reason

\- alternatives considered

\- implications

\- follow-up actions



\---



\# Decision 001 — Use a dedicated GitHub repository



\## Date



2026-06-24



\## Decision



Create a dedicated GitHub repository named:



`zillow-undervalued-property-research`



\## Reason



This project is large enough to require its own version-controlled repo. It will eventually include documentation, notebooks, scripts, source code, raw data samples, processed outputs, and research notes.



\## Alternatives Considered



\- Keep files locally only

\- Add this project inside another data science repo

\- Use Google Drive only



\## Why Those Were Rejected



Local-only storage would make it easier to lose track of changes. A shared miscellaneous repo would become messy. Google Drive is useful for documents but not ideal for version-controlled code.



\## Implications



All important project files should be committed to GitHub, except sensitive files, credentials, large raw files, and ignored data outputs.



\## Follow-up Actions



\- Maintain `.gitignore`

\- Commit changes after each clean milestone

\- Push to GitHub after each session



\---



\# Decision 002 — Use a structured data science project layout



\## Date



2026-06-24



\## Decision



Use a structured folder layout with separate folders for:



\- `data/`

\- `outputs/`

\- `notebooks/`

\- `src/`

\- `scripts/`

\- `docs/`

\- `prompts/`

\- `tests/`



\## Reason



The project will become easier to maintain if raw data, processed data, code, notebooks, documentation, and outputs are separated from the beginning.



\## Alternatives Considered



\- Put everything in one folder

\- Work only in notebooks

\- Delay structure until later



\## Why Those Were Rejected



A loose folder structure would become confusing once the project includes raw Zillow output, normalized data, scoring files, research notes, and dashboards.



\## Implications



New files should be placed intentionally:



\- raw connector output goes in `data/raw/`

\- processed tables go in `data/processed/`

\- charts and reports go in `outputs/`

\- reusable functions go in `src/`

\- one-off scripts go in `scripts/`

\- project documentation goes in `docs/`

\- reusable ChatGPT/Zillow prompts go in `prompts/`



\## Follow-up Actions



\- Keep README updated

\- Keep data dictionary updated

\- Avoid creating random files in the repo root



\---



\# Decision 003 — Treat the project as a research queue, not an investment engine



\## Date



2026-06-24



\## Decision



The project will identify potentially interesting properties for human review. It will not make automatic buy, sell, legal, tax, mortgage, or investment recommendations.



\## Reason



Real estate decisions require human judgment, due diligence, financing assumptions, inspection data, legal review, tax review, and local market knowledge.



\## Alternatives Considered



\- Build an automatic buy/sell recommendation model

\- Use aggressive ranking language like “strong buy”

\- Focus only on score maximization



\## Why Those Were Rejected



That would create false confidence and overstate what Zillow connector data can support.



\## Implications



Output labels should be conservative:



\- Research first

\- Watchlist

\- Avoid

\- Possible candidate after human review

\- Needs data review



Avoid labels such as:



\- Buy

\- Strong buy

\- Guaranteed undervalued

\- Safe investment



\## Follow-up Actions



\- Keep disclaimers in README and scoring methodology

\- Make sure research notes cite actual available evidence

\- Flag missing data rather than guessing



\---



\# Decision 004 — Start with a small MVP before scoring



\## Date



2026-06-24



\## Decision



Do not build the full scoring model immediately.



The first implementation milestone should be:



1\. Pull 10–25 properties.

2\. Save raw Zillow connector output.

3\. Inspect available fields.

4\. Normalize the data into a first dataframe.

5\. Create/update the data dictionary.

6\. Add data-quality flags.

7\. Only then begin scoring.



\## Reason



The project should be based on fields that are actually available from the Zillow connector, not fields we hope are available.



\## Alternatives Considered



\- Build scoring logic immediately

\- Design a complete real estate valuation model before seeing the data

\- Pull hundreds of listings before testing the schema



\## Why Those Were Rejected



Premature scoring would create unstable code and unreliable results. The Zillow connector may not provide every desired field consistently.



\## Implications



The next coding milestone should focus on data availability, normalization, and field inspection.



\## Follow-up Actions



\- Create `docs/zillow\_field\_notes.md`

\- Pull first small Zillow sample

\- Save raw output

\- Update `docs/data\_dictionary.md`

\- Build first normalization script



\---



\# Decision 005 — Use conservative scoring



\## Date



2026-06-24



\## Decision



Use a transparent 100-point MVP score:



\- Valuation: 40 points

\- Income potential: 25 points

\- Property usefulness: 20 points

\- Data quality: 15 points



\## Reason



This keeps the first scoring model simple, explainable, and easy to debug.



\## Alternatives Considered



\- Machine learning model

\- Complex valuation model

\- Heavily weighted rent-yield model

\- Pure Zestimate discount model



\## Why Those Were Rejected



The project does not yet have enough validated data to justify complex scoring.



\## Implications



Missing data should reduce confidence. Missing Zestimate or Rent Zestimate should not automatically exclude a property, but it should reduce confidence.



\## Follow-up Actions



\- Confirm which fields are available

\- Calculate simple derived metrics first

\- Build scoring only after normalized dataframe exists



\---



\# Decision 006 — Validate geography manually using latitude and longitude



\## Date



2026-06-24



\## Decision



Use Zillow search results as the starting point, but validate whether properties are actually within 25 miles of ZIP code 02131 using latitude and longitude in Python.



\## Reason



Connector search areas may not perfectly match a true 25-mile radius.



\## Alternatives Considered



\- Trust Zillow search area directly

\- Search only by ZIP code

\- Search only by city/town



\## Why Those Were Rejected



ZIP and city searches may miss relevant nearby properties or include properties outside the intended radius.



\## Implications



The normalized dataframe should include:



\- latitude

\- longitude

\- distance\_from\_02131\_miles

\- outside\_target\_radius flag



\## Follow-up Actions



\- Add distance calculation in `src/geocoding.py`

\- Add `outside\_target\_radius` data-quality flag

\- Exclude outside-radius properties from the main ranking



\---



\# Decision 007 — Track property lifecycle later



\## Date



2026-06-24



\## Decision



Eventually track listings through:



`for sale → under contract / pending → sold → final sale price recorded`



\## Reason



This turns the project from a one-time screener into a learning system. It allows future comparison between estimated fair value, original list price, last list price, and final sale price.



\## Alternatives Considered



\- Only score active listings once

\- Ignore sold outcomes

\- Update scores without preserving historical predictions



\## Why Those Were Rejected



Without outcome tracking, the model cannot be evaluated honestly over time.



\## Implications



Future tables should include:



\- `property\_status\_history`

\- `valuation\_snapshots`

\- `sale\_outcomes`

\- `model\_evaluation`



Fair value estimates should be frozen before sale outcomes are known.



\## Follow-up Actions



\- Build active-listing normalization first

\- Add scoring second

\- Add valuation snapshots third

\- Add status/outcome tracking after the basic pipeline works



\---



\# Decision 008 — Use Notepad and Anaconda Prompt for early setup



\## Date



2026-06-24



\## Decision



Use Windows Anaconda Prompt and Notepad for the initial setup and documentation files.



\## Reason



This keeps the early workflow simple and avoids overcomplicating setup with IDE configuration.



\## Alternatives Considered



\- Start in Anaconda Desktop

\- Start in VS Code

\- Start in Jupyter immediately



\## Why Those Were Rejected



The first priority is getting the repo, folders, docs, commits, and environment stable.



\## Implications



More advanced tools can be added later after the project scaffold is stable.



\## Follow-up Actions



\- Continue using Anaconda Prompt for Git commands

\- Use Jupyter Lab once the first raw Zillow sample is ready for inspection

\- Add VS Code or Anaconda Desktop later only if helpful



\---



\# Future Decisions to Record



Add new decisions here when they happen:



\- Which Zillow fields are safe for MVP scoring

\- Whether to store data as CSV, SQLite, or both

\- Whether to use Jupyter notebooks or scripts first

\- Whether to add Streamlit dashboard

\- Whether to use public assessor data

\- Whether to add rental-income assumptions

\- Whether to add model versioning

\- Whether to automate weekly refreshes

---

# Decision 013 — Separate candidate gating from scoring

## Date

2026-07-03

## Decision

Create an active-listing candidate table before creating any valuation score.

## Reason

The active Zillow search returns useful search-level records, but it does not consistently return all fields needed for scoring, such as days on market, price history, listing description, tax history, HOA fees, or validated Zestimate/Rent Zestimate fields.

The project should first separate properties into conservative review states before ranking them.

## Alternatives Considered

- Score all active listings immediately
- Use Zestimate discount as the first score
- Treat price per square foot alone as the ranking metric

## Why Those Were Rejected

Premature scoring would overstate what the current data supports.

Price per square foot and Zestimate fields may be useful later, but they are not sufficient by themselves.

## Implications

The project now uses candidate states and review buckets before scoring:

- reject
- hold
- needs_review
- rankable_later

## Follow-up Actions

Next phase should build a conservative valuation/context feature table from validated search-level fields.

Do not build final scoring yet.

---

# Decision 014 — Keep excluded/held candidates visible instead of dropping them

## Date

2026-07-08

## Decision

Add `scripts/create_candidate_exclusion_review_table.py`, producing
`data/interim/candidate_exclusion_review_table.csv` and
`outputs/tables/candidate_exclusion_review_summary.csv`. This table holds
every property whose `candidate_review_bucket` is `reject`, `hold`, or
`needs_review`, with a plain-language reason and a cross-reference to that
property's disposition in the research queue.

Also fixed `.gitignore` so `outputs/reports/*.md` and
`outputs/tables/*summary*.csv` are committable, and removed the empty dead
stub `scripts/create_research_queue.py` (superseded by
`create_research_queue_table.py`).

## Reason

Prior stages already gate out non-rankable properties, but there was no
table that made those exclusions visible for human review. Without one,
a property could be quietly filtered out of every downstream table with no
record of why.

## Alternatives Considered

- Leave excluded/held records implicit in the candidate table only
- Score excluded records as zero instead of explaining the exclusion
- Skip committing audit outputs entirely

## Why Those Were Rejected

Implicit exclusion makes it hard to audit whether the pipeline is dropping
records that deserve a second look once more data is available. Scoring
excluded records as zero would misrepresent missing/invalid data as a
negative signal rather than an unknown. Never committing audit outputs
made it impossible to review pipeline history from git alone.

## Implications

- Reject/hold/needs_review properties are now preserved with an explicit
  reason and next step, not silently dropped.
- Small audit CSVs/reports (not raw or interim data) are committed going
  forward, consistent with the project's `safe_to_commit` policy.

## Follow-up Actions

- Build the property research notes stage (`outputs/property_research_notes/`)
  once the exclusion review table has been used in a real run.
- Consider adding `config/*.yml` files for geography, field mapping, and
  data-quality rules instead of hardcoding thresholds in scripts.

---

# Decision 015 — Complete the MVP: property research notes and MVP run summary

## Date

2026-07-12

## Decision

Add `scripts/create_property_research_notes.py`, which generates one
markdown note per non-excluded research-queue property in
`outputs/property_research_notes/`, plus
`outputs/tables/property_research_notes_summary.csv`. Also add
`scripts/create_mvp_run_summary.py`, which rolls up counts across every
pipeline stage into `outputs/reports/mvp_run_summary.md`, distinct from
the earlier `outputs/reports/run_summary.md`.

This completes the MVP pipeline described in the project instructions:

```text
Zillow search-level data -> normalized property table -> data-quality gates
-> candidate table -> valuation/context features -> human-review research queue
-> excluded/hold review table -> property research notes -> MVP run summary
```

## Reason

The research queue and exclusion review table organize properties for
review, but a human reviewer still needs a single readable document per
property that cites available evidence and explicitly lists what is
missing, plus one report that confirms the whole pipeline's anti-overclaim
safeguards are still holding.

## Alternatives Considered

- Skip per-property notes and rely on the research queue CSV alone
- Let each pipeline stage's own summary stand in for a final rollup report
- Generate note text from a template that includes literal words like
  "buy" or "sell" inside negated disclaimer sentences

## Why Those Were Rejected

A CSV row is not the intended human-readable artifact the project
instructions describe. Per-stage summaries do not answer the doc's
review_questions (data quality, valuation context, research queue,
limitations) in one place. Negated disclaimer sentences ("not a buy or
sell recommendation") still contain the literal forbidden words the
project's own language rules ban — the notes generator now enforces this
with a regex check that raises before writing any note containing a
forbidden phrase, so disclaimers were reworded to avoid the literal words
entirely ("not a purchase or sale recommendation").

## Implications

- Every research-queue property except `excluded`-bucket ones now has a
  markdown note with a required section set (property summary, available
  evidence, valuation context, income context, data-quality warnings,
  missing information, next research steps, interpretation cautions).
- `outputs/reports/mvp_run_summary.md` is the report to check at the end
  of a run; all four anti-overclaim counts (final score, investment
  recommendation, buy/sell recommendation, backtesting-ready) must read 0.

## Follow-up Actions

- Consider adding `config/*.yml` files for geography, field mapping, and
  data-quality rules instead of hardcoding thresholds in scripts.
- Add `tests/` coverage for the forbidden-language check and the
  candidate-gating logic before building any real scoring model.
- Do not begin the scoring/status-tracking/backtesting phases until sale
  outcomes can be confirmed, per the project's backtesting rules.

---

# Decision 016 — Close audit gaps found after MVP completion

## Date

2026-08-16

## Decision

Fix four gaps found during a post-MVP audit, all mechanical cleanup rather
than new pipeline logic:

1. `.gitignore` un-ignores `outputs/property_research_notes/*.md` (mirroring
   the existing `outputs/reports/*.md` rule), and the 10 existing notes are
   now tracked in git instead of silently gitignored.
2. `docs/zillow_field_notes.md`'s stale "Current Status" header ("No raw
   Zillow connector sample has been saved yet") is corrected — the rest of
   that document was already a thorough, up-to-date log through Search
   Pull 7 / Detail Probe 6; only the top summary block was wrong.
3. `.env.example` now documents *why* it has no variables yet (no code in
   the repo reads environment variables; data currently enters via
   manually-pasted Zillow-connector-via-ChatGPT output, not a live API)
   instead of being silently empty.
4. Added `tests/test_research_notes_language.py` and
   `tests/test_candidate_gating.py`, closing the outstanding follow-up from
   Decision 015.

## Reason

Decision 015 declared the MVP complete, but the repo's actual git-tracked
state and a stale doc header didn't match that claim, and the decision
log's own follow-up action to add test coverage was still outstanding.

## Alternatives Considered

- Leave the notes gitignored and treat `outputs/property_research_notes/`
  as purely regenerable, like `data/interim/`.
- Rewrite `docs/zillow_field_notes.md` from scratch instead of a targeted
  fix.
- Defer test coverage further, until a scoring model exists.

## Why Those Were Rejected

The research notes are the human-readable deliverable of the MVP (Decision
015's stated goal), not disposable intermediate data — they belong with
`outputs/reports/*.md`, which is already committed. A full rewrite of
`docs/zillow_field_notes.md` would have discarded a genuinely useful,
already-accurate probe log for no benefit. Deferring tests again would
repeat the same gap Decision 015 already flagged and not fixed.

## Implications

- Future notes generated by `scripts/create_property_research_notes.py`
  will be tracked in git automatically.
- `pytest` now covers the forbidden-language regex (including the
  negated-disclaimer case) and the reject/hold/needs_review/rankable_later
  gating order in `scripts/create_active_listing_candidate_table.py`.

## Follow-up Actions

- Keep `config/*.yml` extraction as a nice-to-have, not required.
- Next real milestone is the conservative scoring model (`prompts/23`),
  still gated behind Decisions 004/007/013 until explicitly approved.

