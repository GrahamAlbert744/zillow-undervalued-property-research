\# Zillow Undervalued Property Research



\## Project Purpose



This project is a real estate research workflow for identifying potentially undervalued residential properties within 25 miles of ZIP code 02131 in the Greater Boston / eastern Massachusetts market.



The goal is not to make automatic buy, sell, or investment decisions. The goal is to collect property data, clean it, store it, score properties conservatively, flag risks, and create a ranked research queue for human review.



\## Search Scope



\- Center ZIP code: 02131

\- Radius: 25 miles

\- Primary market: Greater Boston / eastern Massachusetts

\- Property types:

&#x20; - Single-family homes

&#x20; - Condos

&#x20; - Townhomes

&#x20; - Multifamily properties, if available



\## Core Workflow



The project will eventually:



1\. Pull available Zillow connector data.

2\. Save raw property data.

3\. Normalize property records into clean tables.

4\. Track listing history, price history, status changes, and sale outcomes.

5\. Create data-quality flags.

6\. Build a conservative undervaluation score.

7\. Generate a ranked property research queue.

8\. Produce research notes for human review.

9\. Track whether properties move from for sale to under contract to sold.

10\. Compare estimated fair value against final sale price to improve the model over time.



\## Important Guardrails



This project does not provide legal, tax, mortgage, or investment advice.



The screener should be treated as a research assistant, not a decision-maker. If a field is missing, stale, or unreliable, the system should flag it instead of guessing.



Properties should not be recommended for purchase automatically. The output categories should be:



\- Research first

\- Watchlist

\- Avoid

\- Possible candidate after human review



\## Planned Data Sources



Initial source:



\- Zillow connector output through ChatGPT



Possible later sources:



\- Public assessor records

\- Sold comparable data

\- Rent estimates

\- Permit records

\- Flood or climate risk data

\- Manual property notes



\## Planned Outputs



\- `data/raw/` — raw Zillow connector results

\- `data/processed/` — normalized property data

\- `outputs/tables/` — score tables and research queues

\- `outputs/reports/` — run summaries and model reports

\- `outputs/research\_notes/` — AI-assisted property notes

\- `docs/` — data dictionary, scoring methodology, and project notes



\## Project Structure



```text

zillow-undervalued-property-research/

&#x20; README.md

&#x20; .gitignore

&#x20; .env.example

&#x20; requirements.txt



&#x20; data/

&#x20;   raw/

&#x20;   interim/

&#x20;   processed/

&#x20;   universe/



&#x20; outputs/

&#x20;   reports/

&#x20;   tables/

&#x20;   maps/

&#x20;   research\_notes/



&#x20; notebooks/

&#x20;   00\_project\_setup.ipynb

&#x20;   01\_zillow\_connector\_exploration.ipynb



&#x20; src/

&#x20;   zillow\_client.py

&#x20;   geocoding.py

&#x20;   field\_mapping.py

&#x20;   data\_quality.py

&#x20;   scoring.py

&#x20;   text\_features.py

&#x20;   comps.py

&#x20;   valuation.py

&#x20;   status\_tracker.py

&#x20;   outcome\_tracker.py



&#x20; scripts/

&#x20;   run\_zip\_radius\_search.py

&#x20;   build\_property\_database.py

&#x20;   create\_research\_queue.py



&#x20; docs/

&#x20;   project\_plan.md

&#x20;   decision\_log.md

&#x20;   data\_dictionary.md

&#x20;   scoring\_methodology.md

&#x20;   zillow\_field\_notes.md

&#x20;   status\_tracking\_methodology.md



&#x20; prompts/

&#x20;   01\_zillow\_project\_brief.md



&#x20; tests/

