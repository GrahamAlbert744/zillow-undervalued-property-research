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

---

# Decision 017 — Post-review housekeeping: retire legacy script, remove unused folder

## Date

2026-08-16

## Decision

Following a full project review, three small cleanups:

1. Pushed the three then-local commits (Phase B skill/subagent/hook,
   CLAUDE.md, Decision 016) to `origin/main`.
2. Moved `scripts/create_run_summary.py` to
   `scripts/legacy/create_run_summary.py` and added a header noting why it
   is retired.
3. Removed the unused `outputs/research_notes/` stub folder (only ever
   contained `.gitkeep`), distinct from the actually-used
   `outputs/property_research_notes/`.

## Reason

`create_run_summary.py` only summarizes the normalize + data-quality
stages, predates candidate gating/research queue/notes, and is not
referenced by the `run-pipeline` skill or any current doc —
`outputs/reports/mvp_run_summary.md` (Decision 015) is the report actually
checked at the end of a run. `outputs/research_notes/` was never wired to
any script and risked being confused with `outputs/property_research_notes/`.

## Alternatives Considered

- Delete `create_run_summary.py` outright instead of moving it.
- Leave both unused items in place indefinitely.

## Why Those Were Rejected

The script still runs and produces a valid (if narrower) report; deleting
it would discard working code for no benefit when moving it to `legacy/`
with an explanatory header preserves it for manual/diagnostic use while
making its non-current status explicit. Leaving unused items in place adds
confusion for no benefit — this is exactly the kind of drift Decision 016's
audit was meant to catch.

## Implications

- `scripts/legacy/` now exists as a convention for retired-but-kept scripts.
- Repo history is on GitHub, not just local, as of this decision.

## Follow-up Actions

- Proceed to `config/*.yml` extraction (Decision log item repeatedly
  deferred since Decision 014).
- Proceed to the conservative scoring model, now explicitly approved.

---

# Decision 018 — Extract shared constants into `config/*.yml`

## Date

2026-08-16

## Decision

Add `config/geography.yml`, `config/forbidden_language.yml`, and
`config/field_mapping.yml`, plus a loader (`src/config.py`), and update
`src/geocoding.py`, `src/field_mapping.py`,
`scripts/create_property_research_notes.py`, and
`scripts/hooks/check_forbidden_language.py` to read from them instead of
inline constants. No values changed — same ZIP/radius, same forbidden
phrases, same home-type mapping.

## Reason

The review that led to Decision 017 found the target ZIP/radius and
lat/long origin hardcoded in `src/geocoding.py` and referenced by name
across roughly a dozen scripts, and — more importantly — the
forbidden-language regex list duplicated verbatim in both
`scripts/create_property_research_notes.py` (the generation-time check) and
`scripts/hooks/check_forbidden_language.py` (the edit-time hook added in
Phase B). Two copies of the project's core guardrail pattern list meant a
future edit to one could silently fail to reach the other. This had been
flagged as a nice-to-have in Decisions 014, 015, and 016 without being
done.

## Alternatives Considered

- Leave the duplication in place since both copies currently match.
- Have the hook import directly from
  `scripts/create_property_research_notes.py` instead of a shared config
  file.
- Extract all of `src/field_mapping.py`'s field-extraction logic into YAML,
  not just the `home_type` label mapping.

## Why Those Were Rejected

Matching today doesn't prevent drift tomorrow — that's the whole risk this
closes. Importing the hook from the notes-generation script would pull in
`pandas` and the rest of that script's machinery into a hook meant to run
fast on every Write/Edit; a shared, dependency-light YAML file is a cleaner
split. Most of `field_mapping.py`'s logic is fallback chains over nested
Zillow connector paths (e.g. try `record["price"]`, then
`hdpData.homeInfo.price`), which is genuinely code, not a lookup table —
forcing it into YAML would add indirection without reducing duplication;
only the one real lookup table (`home_type` labels) was extracted.

## Implications

- A future change to the banned-phrase list, the target radius, or a
  home-type label variant is a one-file edit that automatically reaches
  every consumer.
- `PyYAML` (already listed in `requirements.txt`) is now an active runtime
  dependency, not just a declared one — installed in the environment used
  to run pipeline scripts.
- Verified byte-identical pipeline output before/after this change (only
  `outputs/reports/mvp_run_summary.md`'s run timestamp differed); `pytest`
  passes, including new `tests/test_config.py`, which regression-tests that
  the notes generator and the hook compile the identical pattern list.

## Follow-up Actions

- None outstanding; config extraction is closed.
- Proceed to the conservative scoring model.

---

# Decision 019 — Build the first conservative scoring model

## Date

2026-08-17

## Decision

Implement `src/scoring.py` (version `score_v0_1_mvp_simple`) and
`scripts/create_property_scores_table.py`, applying the 100-point MVP
framework already specced in `docs/scoring_methodology.md` — Valuation
(40), Income Potential (25), Property Usefulness (20), Data Quality (15) —
to every property already past candidate gating. This begins the milestone
Decisions 004, 007, and 013 gated behind explicit approval, given here.

The new stage runs between `create_valuation_context_features.py` and
`create_research_queue_table.py`. `create_research_queue_table.py` now
reads `data/interim/property_scores.csv` instead of
`valuation_context_features.csv` directly, and uses `total_research_score`
as an added tiebreaker in the existing queue ordering — it does not change
which `research_priority`/`research_queue_bucket` a property falls into,
only the order within a bucket. No new output-label vocabulary was
introduced; the score is exposed only as numeric columns and confidence
notes, not as a category label, since the doc's own "Preliminary Score
Categories" table (e.g. "Strong research candidate") uses terms outside
CLAUDE.md's allowed output-label list and this project already has an
unresolved gap between that allowed-label list and the labels the pipeline
actually emits (`review_first`, `watchlist_limited_data`, etc.) — not a gap
this decision should widen further. See Follow-up Actions.

Only 82 of the 100 possible points are achievable in this version; the
doc's own "future feature" signals (comparable-sale discount, price-cut/
days-on-market history, HOA/tax burden, multifamily rental-use potential)
are not implemented and always score 0. `docs/scoring_methodology.md` and
`outputs/reports/mvp_run_summary.md` both document this explicitly.

## Reason

The candidate-gating, valuation-context, and research-queue stages were
already validated on the real (if small) sample data, satisfying the
condition Decisions 004/007/013 set for starting scoring. The methodology
document had already fully specified the MVP model; this decision
implements it rather than redesigning it.

## Alternatives Considered

- Use `prompts/23_conservative_scoring_model.md`'s point breakdown
  (40/20/15/15/10) instead of `docs/scoring_methodology.md`'s (40/25/20/15).
- Score every normalized record, including `reject`/`hold` candidate-gating
  buckets.
- Emit the doc's "Preliminary Score Categories" labels (Strong research
  candidate / Research candidate / Low priority / etc.) as an output field.
- Treat the four existing anti-overclaim flags
  (`final_score_created`/`investment_recommendation_created`/
  `buy_sell_recommendation_created`/`backtesting_ready`) as satisfied by
  simply flipping `final_score_created` to `True` now that a score exists.

## Why Those Were Rejected

`prompts/23` predates Decision 013's candidate-gating split and is the
older of the two specs; `docs/scoring_methodology.md` is the doc the
project's own "Current Status" section pointed to as still being iterated
on, and is more detailed. Scoring `reject`/`hold` records would contradict
Decision 013's whole premise — those records are already conservatively
routed to `candidate_exclusion_review_table.csv` instead. The doc's
category labels are not on CLAUDE.md's allowed-label list, and introducing
a third informal label vocabulary (alongside the doc's allowed list and the
pipeline's actual bucket names) would make an existing documentation gap
worse instead of narrowing it — pure numeric score + confidence notes
avoids that entirely. Flipping `final_score_created` to `True` would be
factually accurate but misleading in intent: this project's own
"Interpretation rule" (`docs/scoring_methodology.md`) distinguishes a
provisional *research-ranking* score from a *final/validated* score, and
that flag exists specifically to signal the latter has not happened —
so a new `research_score_created` flag was added instead, and the original
four flags keep their original meaning and stay `False`.

## Implications

- `outputs/tables/undervaluation_scores_summary.csv` and
  `data/interim/property_scores.csv` now exist; see
  `docs/data_dictionary.md`.
- `outputs/reports/mvp_run_summary.md` has a new "Research Scoring"
  section, and its "Limitations" section now explains the 82-of-100 ceiling
  instead of stating no scoring model has been built.
- Verified via a full pipeline run: research-queue bucket counts
  (`review_first`/`review_next`/etc.) are unchanged from the pre-scoring
  run — only within-bucket ordering can change — and all four
  Anti-Overclaim Safeguards counts still read 0.
- `tests/test_scoring.py` added, covering: total score never exceeds the
  82-point ceiling, missing data never inflates a component score,
  `reject`/`hold` rows are never scored, and the scoring stage never sets
  `fair_value_estimate_created`/`investment_recommendation_created`/
  `buy_sell_recommendation_created`/`backtesting_ready`.

## Follow-up Actions

- CLAUDE.md's allowed output-label list
  (`research first`/`watchlist`/`avoid`/`possible candidate after human
  review`/`needs data review`) is not yet implemented anywhere in the
  pipeline; the research-queue buckets use different internal names. This
  predates this decision and this decision does not fix it, but it should
  be resolved before any user-facing label (score-derived or otherwise) is
  added.
- Consider adding the doc's remaining deferred signals (comparable-sale
  discount once a comp engine exists, price-cut/days-on-market once detail
  pulls are relied on, HOA/tax burden, multifamily rental-use potential) as
  their own future scoring-version decisions, each bumping the version
  number per the doc's Versioning Rules.
- Per Decisions 007/013's original sequencing and the doc's Model
  Evaluation Metrics section, do not begin status/lifecycle tracking or
  backtesting until sale outcomes are confirmable, and do not calibrate
  this score's thresholds with fewer than 20 sold outcomes.

