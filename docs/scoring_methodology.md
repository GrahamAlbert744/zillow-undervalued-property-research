\# Scoring Methodology



\## Purpose



This document defines the planned scoring approach for the Zillow Undervalued Property Research project.



The goal is not to automatically recommend buying or selling properties. The goal is to create a conservative, transparent research score that helps rank properties for further human review.



The model should be treated as a screening tool, not an investment decision engine.



\---



\## Core Principle



Missing data should reduce confidence.



Missing data should not make a property look more attractive.



A property should only receive a strong score when it has clear positive signals and enough data to support those signals.



\---



\## MVP Scoring Model



The first scoring model will use a simple 100-point framework.



| Category | Points | Purpose |

|---|---:|---|

| Valuation | 40 | Identify properties that appear cheap relative to available value signals. |

| Income Potential | 25 | Identify properties with potentially attractive rental economics. |

| Property Usefulness | 20 | Reward properties with useful size, layout, and property type characteristics. |

| Data Quality | 15 | Reward complete and reliable records; penalize missing or suspicious data. |



Total possible score: 100 points.



\---



\# 1. Valuation Score — 40 Points



The valuation score should estimate whether a property appears inexpensive relative to available benchmarks.



\## Planned valuation signals



| Signal | Points | Notes |

|---|---:|---|

| Price per square foot relative to local median | 20 | Use only after enough local records exist. |

| Price below Zestimate, if available | 10 | Use cautiously; Zestimate is not ground truth. |

| Price cut or stale listing signal | 5 | Only if days-on-market or price-history data is available. |

| Discount to comparable sales estimate | 5 | Future feature; do not use until comp engine is built. |



\## MVP valuation rules



For the first version, prioritize:



1\. `price\_per\_sqft`

2\. local median `price\_per\_sqft`

3\. `price\_to\_zestimate\_pct`, if Zestimate is available

4\. basic outlier flags



Do not calculate a serious fair value estimate until comparable-sale logic is available.



\---



\# 2. Income Potential Score — 25 Points



The income score should estimate whether a property may have attractive rental economics.



\## Planned income signals



| Signal | Points | Notes |

|---|---:|---|

| Rent Zestimate available | 5 | Availability increases confidence. |

| Gross rent yield | 12 | Annual rent estimate divided by listing price. |

| HOA/tax burden | 4 | Future feature; important for condos. |

| Multifamily or rental-use potential | 4 | Future feature; requires validation. |



\## MVP income rules



For the first version, use only:



1\. `rent\_zestimate`, if available

2\. `annual\_rent\_zestimate`

3\. `gross\_rent\_yield`



Do not calculate cap rate, cash-on-cash return, or DSCR until taxes, insurance, HOA, maintenance, vacancy, and financing assumptions are added.



\---



\# 3. Property Usefulness Score — 20 Points



This score rewards properties that are more useful, liquid, or interpretable for screening.



\## Planned usefulness signals



| Signal | Points | Notes |

|---|---:|---|

| Valid square footage | 5 | Required for price-per-square-foot analysis. |

| Valid beds and baths | 5 | Needed for comparison and usability. |

| Residential property type | 5 | Single-family, condo, townhome, multifamily. |

| Useful size/layout | 5 | Future refinement after data inspection. |



\## MVP usefulness rules



Reward properties that have:



\- valid square footage

\- valid beds

\- valid baths

\- valid home type

\- valid listing price



Flag land, unknown property type, or records with missing core facts.



\---



\# 4. Data Quality Score — 15 Points



The data-quality score should prevent incomplete or suspicious records from ranking too highly.



\## Planned data-quality signals



| Signal | Points | Notes |

|---|---:|---|

| Core fields complete | 5 | Price, sqft, beds, baths, type, address. |

| Valid geocode | 3 | Latitude and longitude available. |

| Inside target radius | 3 | Must be within 25 miles of 02131. |

| No duplicate warning | 2 | Avoid duplicate listings. |

| No suspicious value warning | 2 | Avoid impossible price/sqft records. |



\## Data-quality penalties



Apply penalties for:



\- missing price

\- missing square footage

\- missing beds

\- missing baths

\- missing property type

\- missing latitude/longitude

\- outside 25-mile radius

\- duplicate address

\- duplicate coordinates

\- suspiciously low price per square foot

\- suspiciously high price per square foot

\- stale listing data

\- missing Zestimate

\- missing Rent Zestimate

\- missing HOA fee for condos

\- unclear listing status



Missing Zestimate or Rent Zestimate should reduce confidence, but should not automatically exclude a property.



\---



\# Preliminary Score Categories



Use these categories for interpretation.



| Score Range | Label | Meaning |

|---|---|---|

| 85–100 | Strong research candidate | Appears attractive and data quality is strong. |

| 70–84 | Research candidate | Worth reviewing manually. |

| 55–69 | Watchlist | Some useful signals but incomplete or mixed evidence. |

| 40–54 | Low priority | Weak score or too many missing fields. |

| 0–39 | Avoid / insufficient data | Not enough evidence or too many red flags. |



Do not call any property a “buy” based on this score.



\---



\# Research Queue Labels



The final output should use conservative labels:



\- Research first

\- Watchlist

\- Avoid

\- Possible candidate after human review

\- Needs data review



Do not use:



\- Buy

\- Strong buy

\- Guaranteed undervalued

\- Safe investment

\- No-risk opportunity



\---



\# Hard Filters



Properties should be excluded from the main ranking if:



\- listing price is missing

\- property is not residential

\- latitude/longitude are missing and distance cannot be validated

\- property is outside 25 miles of ZIP code 02131

\- square footage is missing and price-per-square-foot cannot be calculated

\- price is zero, negative, or obviously invalid

\- property appears duplicated and cannot be resolved

\- listing status is unclear enough to make the record unreliable



Excluded properties should still be saved in an excluded-properties table or data-quality report.



\---



\# Soft Ranking Signals



Properties may receive higher priority if they show:



\- low price per square foot relative to similar local listings

\- list price below Zestimate, if available

\- rent estimate suggesting attractive gross yield

\- recent price cut

\- high days on market

\- complete core data

\- valid geocode

\- residential property type

\- useful size/layout

\- text suggesting cosmetic issues rather than structural issues



Properties should receive lower priority if they show:



\- high HOA fee

\- missing square footage

\- missing beds/baths

\- missing property type

\- suspiciously low or high price per square foot

\- bad or missing coordinates

\- major repair language

\- structural issue language

\- cash-only language

\- flood, fire, mold, foundation, or water-damage language



\---



\# Listing Text Signals



Listing text should be used conservatively.



The model may flag positive opportunity signals such as:



\- needs TLC

\- fixer upper

\- estate sale

\- motivated seller

\- price reduced

\- cosmetic updates

\- expansion potential

\- unfinished basement

\- large lot



The model may flag serious risk signals such as:



\- foundation issue

\- water damage

\- mold

\- fire damage

\- failed septic

\- cash only

\- structural issue

\- no financing

\- special assessment

\- tenant occupied with restrictions



Text analysis should only flag phrases that are actually present. It should not infer hidden property conditions.



\---



\# Future Valuation Model



After the MVP is stable, add a more serious fair value model using:



\- recent sold comps

\- property type

\- beds

\- baths

\- square footage

\- location

\- sale date

\- price per square foot

\- listing status

\- price cut history

\- tax assessment, if available

\- Zestimate, if available



The fair value model should return:



\- estimated fair value

\- estimated discount percentage

\- confidence level

\- comparable-property notes

\- missing-data warnings



\---



\# Lifecycle and Outcome Learning



The project should eventually track each property over time:



\- for sale

\- price reduced

\- under contract

\- pending

\- sold

\- off market

\- unknown / needs manual review



Each estimated fair value should be saved as a frozen valuation snapshot.



When the property later sells, compare:



\- estimated fair value at time of prediction

\- original list price

\- last list price before contract

\- final sale price



The model should not retroactively change old predictions after the sale. Each scoring rule change should create a new model version.



This prevents look-ahead bias and allows the model to be evaluated honestly.



\---



\# Model Evaluation Metrics



Once enough sold outcomes exist, evaluate:



\- mean absolute prediction error

\- median absolute prediction error

\- mean bias

\- percent of predictions within 5%

\- percent within 10%

\- percent within 15%

\- accuracy by property type

\- accuracy by city

\- accuracy by price band

\- accuracy by data-quality tier

\- accuracy by score bucket



Do not update scoring thresholds based on too few sold properties.



Suggested rule:



\- fewer than 20 sold outcomes: observe only

\- 20–50 sold outcomes: exploratory calibration

\- 50+ sold outcomes: consider minor model updates

\- 100+ sold outcomes: more serious calibration review



\---



\# Versioning Rules



Every scoring model should have a version number.



Example:



\- `score\_v0\_1\_mvp\_simple`

\- `score\_v0\_2\_added\_rent\_yield`

\- `score\_v0\_3\_added\_status\_tracking`

\- `score\_v1\_0\_comp\_based\_model`



Each version should record:



\- date introduced

\- scoring changes

\- reason for change

\- fields used

\- known limitations

\- validation results, if available



\---



\# Current Status



This methodology is a planning document.



The next step is not to score properties. The next step is to inspect actual Zillow connector fields, update the data dictionary, and determine which fields are reliable enough for MVP scoring.

