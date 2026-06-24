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

