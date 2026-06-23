\# Zillow Undervalued Property Research Project Plan



\## Project Purpose



This project is a real estate research workflow for identifying potentially undervalued residential properties within 25 miles of ZIP code 02131.



The goal is not to make automatic buy, sell, legal, tax, or mortgage recommendations. The goal is to collect available property data, clean it, store it, score it conservatively, flag risks, and create a ranked research queue for human review.



\## Search Scope



\- Center ZIP code: 02131

\- Radius: 25 miles

\- Primary market: Greater Boston / eastern Massachusetts

\- Property types:

&#x20; - Single-family homes

&#x20; - Condos

&#x20; - Townhomes

&#x20; - Multifamily properties, if available



\## MVP Goal



The first working version should be intentionally small.



The MVP should:



1\. Pull a small Zillow connector sample.

2\. Save the raw output.

3\. Inspect available fields.

4\. Normalize the data into a first dataframe.

5\. Create data-quality flags.

6\. Export a clean CSV.

7\. Create an initial data dictionary.

8\. Avoid full scoring until field availability is understood.



\## First Dataframe Fields



The first normalized property dataframe should aim to include:



\- zpid

\- address

\- city

\- state

\- zip\_code

\- latitude

\- longitude

\- home\_status

\- status\_text

\- home\_type

\- price

\- zestimate, if available

\- rent\_zestimate, if available

\- beds

\- baths

\- square\_feet

\- lot\_size, if available

\- price\_per\_sqft

\- price\_to\_zestimate\_pct, if available

\- estimated\_gross\_rent\_yield, if available

\- zillow\_url

\- search\_date

\- data\_source



\## Data-Quality Flags



Create data-quality flags before building a serious scoring model.



Initial flags:



\- missing\_price

\- missing\_square\_feet

\- missing\_beds

\- missing\_baths

\- missing\_home\_type

\- missing\_lat\_long

\- missing\_zestimate

\- missing\_rent\_zestimate

\- undisclosed\_address

\- possible\_duplicate\_address

\- possible\_duplicate\_lat\_long

\- invalid\_price

\- invalid\_square\_feet

\- suspiciously\_low\_price\_per\_sqft

\- suspiciously\_high\_price\_per\_sqft

\- outside\_target\_radius

\- new\_construction\_flag

\- data\_needs\_review



\## Conservative Scoring Philosophy



The first score should be simple, transparent, and conservative.



Missing data should reduce confidence. Missing data should not make a property appear more attractive.



Initial MVP score idea:



\- Valuation score: 40 points

\- Income potential score: 25 points

\- Property usefulness score: 20 points

\- Data-quality score: 15 points



Do not build the final scoring model until the first Zillow connector sample has been inspected.



\## Lifecycle Tracking



The project should eventually track property status over time:



\- for sale

\- price reduced

\- under contract

\- pending

\- sold

\- off market

\- unknown / needs manual review



Each estimated fair value should eventually be saved as a frozen valuation snapshot. If the property later sells, the final sale price should be compared against the earlier estimated fair value.



This allows the project to evaluate whether the model is too optimistic, too conservative, or reasonably calibrated.



\## Planned Outputs



Initial outputs:



\- data/raw/zillow\_raw\_search\_YYYYMMDD.json

\- data/processed/all\_properties\_normalized.csv

\- outputs/tables/property\_data\_quality\_report.csv

\- outputs/tables/undervaluation\_scores.csv

\- outputs/tables/top\_25\_property\_research\_queue.csv

\- outputs/tables/excluded\_properties.csv

\- outputs/reports/run\_summary.md

\- docs/data\_dictionary.md

\- docs/scoring\_methodology.md

\- docs/zillow\_field\_notes.md



\## Build Sequence



1\. Confirm local folder, conda environment, GitHub repo, and project scaffold.

2\. Create README and core docs.

3\. Pull a small Zillow connector sample.

4\. Save raw Zillow output.

5\. Inspect fields.

6\. Build field mapping.

7\. Normalize to a dataframe.

8\. Create data-quality flags.

9\. Export first clean CSV.

10\. Create data dictionary.

11\. Only then begin simple scoring.

12\. Later add lifecycle tracking, sale outcomes, dashboard, and model backtesting.



\## Current Status



Project setup is underway.



Completed:



\- Local project folder

\- Conda environment

\- GitHub repo

\- Project scaffold

\- README



Current step:



\- Create core documentation files



Next step:



\- Create data dictionary, scoring methodology, Zillow field notes, and decision log.

