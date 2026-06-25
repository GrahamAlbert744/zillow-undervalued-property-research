\# Data Dictionary



\## Purpose

---

# Observed MVP Pipeline Fields

## Source

These fields come from the first local Zillow sample and normalization pipeline.

Pipeline flow:

```text
data/raw/zillow_raw_search_20260624.json
→ src/field_mapping.py
→ data/processed/all_properties_normalized.csv
→ src/data_quality.py
→ outputs/tables/
→ outputs/reports/run_summary.md

This section reflects the first working pipeline and should be updated as the Zillow connector sample expands.

Table: all_properties_normalized.csv

One row per Zillow property/listing record.

Field	Type	Source / Derivation	MVP Use	Notes
property_id	text	Derived from Zillow ZPID	Core identifier	Same as zpid for now.
zpid	text	Zillow URL or raw field	Core identifier	Best available property/listing identifier.
address	text	Raw address fields	Core field	May be undisclosed or incomplete.
city	text	Raw city field	Core field	Observed values include Roslindale and Boston.
state	text	Raw state field	Core field	Expected MA.
zip_code	text	Raw postal code	Core field	Store as text, not numeric.
latitude	numeric	Raw geocode field	Geography validation	Required for radius filtering.
longitude	numeric	Raw geocode field	Geography validation	Required for radius filtering.
is_bad_geocode	boolean	Raw Zillow geocode flag	Data-quality check	Use to flag bad geocodes if available.
home_status	text	Raw or normalized listing status	Future lifecycle tracking	Search-level output may not always provide this.
status_text	text	Raw or simplified status label	Future lifecycle tracking	Useful but not reliable enough for sold/pending logic yet.
home_type	text	Normalized from raw home type	Core field	Expected values: single_family, condo, townhome, multi_family.
fixture_classification	text	Raw connector field	Data-quality context	Observed values include unit, improvement, representative.
price	numeric	Raw listing price	Core field	Required for MVP.
zestimate	numeric	Not observed in basic search output	Not safe yet	Keep as nullable; requires detail pull validation.
rent_zestimate	numeric	Not observed in basic search output	Not safe yet	Keep as nullable; requires detail pull validation.
beds	numeric	Raw bedroom count	Core field	Used for property description and later metrics.
baths	numeric	Raw bathroom count	Core field	Used for property description and later metrics.
square_feet	numeric	Raw living area	Core field	Required for price-per-square-foot.
lot_size	numeric	Raw lot area if available	Optional field	Often missing for condos or units.
lot_size_units	text	Raw lot units	Optional field	Observed as Square Feet or Acres.
price_per_sqft	numeric	price / square_feet	MVP metric	Safe only when price and square footage are valid.
price_to_zestimate_pct	numeric	(price - zestimate) / zestimate	Paused	Not useful until Zestimate is validated.
annual_rent_zestimate	numeric	rent_zestimate * 12	Paused	Not useful until Rent Zestimate is validated.
gross_rent_yield	numeric	annual_rent_zestimate / price	Paused	Not useful until Rent Zestimate is validated.
new_construction_available_plan_count	numeric	Raw new construction field	Data-quality context	Helps identify plans/new construction.
new_construction_premier_builder	boolean	Raw new construction field	Data-quality context	May identify builder listings.
has_open_house	boolean	Raw connector field	Optional context	Not a valuation signal yet.
has_vr_model	boolean	Raw connector field	Optional context	Not a valuation signal yet.
title	text	Raw title field	Optional context	Often condo/building/community name.
zillow_url	text	Raw Zillow URL	Core field	Required for manual review.
search_date	date/text	Raw metadata	Run tracking	Date sample was created or pulled.
data_source	text	Assigned by pipeline	Run tracking	Currently zillow_connector.
Data-Quality Flag Fields
Field	Type	Meaning	Action
missing_price	boolean	Listing price is missing.	Exclude from main ranking.
missing_square_feet	boolean	Square footage is missing.	Exclude or place in review queue.
missing_beds	boolean	Bedroom count is missing.	Flag for review.
missing_baths	boolean	Bathroom count is missing.	Flag for review.
missing_home_type	boolean	Property type is missing.	Exclude or review.
missing_lat_long	boolean	Latitude or longitude missing.	Cannot validate radius; review or exclude.
missing_zestimate	boolean	Zestimate missing.	Expected for search-level output; do not penalize too heavily yet.
missing_rent_zestimate	boolean	Rent Zestimate missing.	Expected for search-level output; income scoring paused.
undisclosed_address	boolean	Address includes undisclosed-address language.	Manual review.
invalid_price	boolean	Price missing, zero, or invalid.	Exclude from ranking.
invalid_square_feet	boolean	Square footage missing, zero, or invalid.	Exclude from price-per-square-foot calculations.
possible_duplicate_address	boolean	Same address appears more than once.	Review before deduplication.
possible_duplicate_lat_long	boolean	Same coordinates appear more than once.	May be separate units; review carefully.
data_needs_review	boolean	One or more major data-quality issues found.	Place in review queue.
MVP Trust Rules
Safe for current MVP inspection
address
city
state
zip_code
latitude
longitude
home_type
price
beds
baths
square_feet
lot_size, if present
lot_size_units, if present
price_per_sqft
zillow_url
Available but use cautiously
fixture_classification
title
new_construction_available_plan_count
new_construction_premier_builder
has_open_house
has_vr_model
home_status
status_text
Not safe for MVP scoring yet
zestimate
rent_zestimate
price_to_zestimate_pct
annual_rent_zestimate
gross_rent_yield
days on market
price history
tax history
sale history
listing description
HOA fee
property tax

These fields either were not returned in the basic search-level output or require property-detail validation.

This document defines the planned fields for the Zillow Undervalued Property Research project.



The data dictionary will start as a planned schema. After the first Zillow connector pull, each field should be updated with its actual availability, source path, reliability, and cleaning rules.



The first goal is not to build a perfect database. The first goal is to create a clean, updateable property dataframe with one row per property/listing.



\---



\# Table: `properties\_normalized`



Primary dataframe for active Zillow listing research.



| Field Name | Type | Required for MVP? | Description | Source | Data Quality Notes |

|---|---:|---:|---|---|---|

| `property\_id` | string | Yes | Internal stable property identifier. Prefer Zillow ZPID if available; otherwise generated from address/source. | Derived | Must be unique. |

| `zpid` | string | Preferred | Zillow property ID, if available. | Zillow | Best unique ID if available. |

| `address` | string | Yes | Full street address. | Zillow | Flag if missing, partial, or undisclosed. |

| `city` | string | Yes | City or town. | Zillow | Normalize spelling and casing. |

| `state` | string | Yes | State abbreviation. | Zillow | Should be `MA` for this project. |

| `zip\_code` | string | Yes | Property ZIP code. | Zillow | Store as text to preserve leading zeros. |

| `latitude` | float | Yes | Latitude coordinate. | Zillow | Needed for distance filter. |

| `longitude` | float | Yes | Longitude coordinate. | Zillow | Needed for distance filter. |

| `distance\_from\_02131\_miles` | float | Yes | Distance from ZIP 02131 anchor point. | Derived | Used to enforce 25-mile radius. |

| `home\_status` | string | Yes | Raw or normalized listing status. | Zillow | Examples: for sale, pending, sold, off market. |

| `status\_text` | string | No | Human-readable listing status text. | Zillow | Useful for lifecycle tracking. |

| `home\_type` | string | Yes | Property type. | Zillow | Examples: singleFamily, condo, townhome, multiFamily. |

| `price` | integer | Yes | Current listing price. | Zillow | Must be positive and plausible. |

| `zestimate` | integer | No | Zillow estimated home value, if available. | Zillow | Do not treat as ground truth. |

| `rent\_zestimate` | integer | No | Zillow estimated monthly rent, if available. | Zillow | Used only when available. |

| `beds` | float | Yes | Number of bedrooms. | Zillow | Flag if missing. |

| `baths` | float | Yes | Number of bathrooms. | Zillow | Flag if missing. |

| `square\_feet` | integer | Yes | Interior living area. | Zillow | Needed for price per square foot. |

| `lot\_size` | float | No | Lot size. | Zillow | Units may vary; normalize later. |

| `lot\_size\_units` | string | No | Lot size units. | Zillow | Examples: sqft, acres. |

| `year\_built` | integer | No | Year property was built. | Zillow/details/public records | Validate if available. |

| `hoa\_fee\_monthly` | float | No | HOA or condo fee per month. | Zillow/details/manual | Important for condos; often missing. |

| `annual\_property\_tax` | float | No | Annual property tax. | Zillow/details/public records | Requires validation. |

| `price\_per\_sqft` | float | Yes | Listing price divided by square feet. | Derived | Missing if price or sqft unavailable. |

| `price\_to\_zestimate\_pct` | float | No | `(price - zestimate) / zestimate`. | Derived | Only calculate when Zestimate exists. |

| `annual\_rent\_zestimate` | float | No | `rent\_zestimate \* 12`. | Derived | Only calculate when rent Zestimate exists. |

| `gross\_rent\_yield` | float | No | `annual\_rent\_zestimate / price`. | Derived | Crude income screen only. |

| `days\_on\_zillow` | integer | No | Days on Zillow/listing age. | Zillow | Useful if available. |

| `price\_cut\_amount` | float | No | Dollar amount of price reduction. | Zillow/details/history | Optional for MVP. |

| `price\_cut\_pct` | float | No | Price cut as percent of prior price. | Derived | Optional for MVP. |

| `listing\_description` | string | No | Listing description text. | Zillow/details | Used for conservative text features. |

| `zillow\_url` | string | Yes | URL to Zillow listing/details page. | Zillow | Useful for manual review. |

| `data\_source` | string | Yes | Source of the record. | Derived | Example: `zillow\_connector`. |

| `search\_date` | date | Yes | Date the record was pulled. | Derived | Required for refresh tracking. |

| `raw\_record\_path` | string | No | Path to saved raw JSON source. | Derived | Useful for auditability. |



\---



\# Table: `data\_quality\_flags`



One row per property/listing, or merged onto `properties\_normalized`.



| Field Name | Type | Description |

|---|---:|---|

| `property\_id` | string | Internal property ID. |

| `missing\_price` | boolean | True if listing price is missing. |

| `missing\_square\_feet` | boolean | True if square footage is missing. |

| `missing\_beds` | boolean | True if bedrooms are missing. |

| `missing\_baths` | boolean | True if bathrooms are missing. |

| `missing\_home\_type` | boolean | True if property type is missing. |

| `missing\_lat\_long` | boolean | True if latitude or longitude is missing. |

| `missing\_zestimate` | boolean | True if Zestimate is missing. |

| `missing\_rent\_zestimate` | boolean | True if Rent Zestimate is missing. |

| `undisclosed\_address` | boolean | True if address is unavailable or incomplete. |

| `possible\_duplicate\_address` | boolean | True if same address appears more than once. |

| `possible\_duplicate\_lat\_long` | boolean | True if same coordinates appear for multiple records. |

| `invalid\_price` | boolean | True if price is zero, negative, or implausible. |

| `invalid\_square\_feet` | boolean | True if square footage is zero, negative, or implausible. |

| `suspiciously\_low\_price\_per\_sqft` | boolean | True if price per square foot is unusually low. |

| `suspiciously\_high\_price\_per\_sqft` | boolean | True if price per square foot is unusually high. |

| `outside\_target\_radius` | boolean | True if property is more than 25 miles from 02131 anchor. |

| `new\_construction\_flag` | boolean | True if listing appears to be new construction. |

| `data\_needs\_review` | boolean | True if one or more important fields require manual review. |



\---



\# Table: `valuation\_metrics`



Derived valuation and income metrics.



| Field Name | Type | Description |

|---|---:|---|

| `property\_id` | string | Internal property ID. |

| `price\_per\_sqft` | float | Listing price divided by square feet. |

| `local\_median\_price\_per\_sqft` | float | Median price per square foot for comparable local group. |

| `price\_per\_sqft\_discount\_pct` | float | Discount or premium versus local median. |

| `price\_to\_zestimate\_pct` | float | Percent difference between list price and Zestimate. |

| `gross\_rent\_yield` | float | Annual rent estimate divided by list price. |

| `estimated\_fair\_value` | float | Conservative fair value estimate. Future field. |

| `estimated\_discount\_pct` | float | Percent discount versus estimated fair value. Future field. |

| `valuation\_confidence` | string | High, medium, low, or insufficient data. |



\---



\# Table: `scores`



Future scoring table. Do not rely on this until the first normalized dataframe is stable.



| Field Name | Type | Description |

|---|---:|---|

| `property\_id` | string | Internal property ID. |

| `valuation\_score` | float | Score for valuation attractiveness. |

| `income\_score` | float | Score for rent/income potential. |

| `property\_usefulness\_score` | float | Score for beds, baths, size, and property type. |

| `data\_quality\_score` | float | Score for data completeness and reliability. |

| `risk\_penalty` | float | Penalty for missing data, suspicious data, or major risk signals. |

| `total\_score` | float | Overall conservative screen score. |

| `score\_version` | string | Version of scoring rules used. |

| `score\_notes` | string | Plain-English explanation of score. |

| `created\_at` | datetime | Timestamp when score was created. |



\---



\# Table: `property\_status\_history`



Future lifecycle tracking table.



| Field Name | Type | Description |

|---|---:|---|

| `status\_history\_id` | string | Unique status record ID. |

| `property\_id` | string | Internal property ID. |

| `zpid` | string | Zillow property ID, if available. |

| `observed\_date` | date | Date status was observed. |

| `listing\_status` | string | Normalized status. |

| `status\_text` | string | Raw status text. |

| `list\_price` | integer | Price observed on this date. |

| `is\_active` | boolean | True if property is actively listed. |

| `is\_under\_contract` | boolean | True if under contract or contingent. |

| `is\_pending` | boolean | True if pending. |

| `is\_sold` | boolean | True if confirmed sold. |

| `is\_off\_market` | boolean | True if off market. |

| `source\_url` | string | Zillow URL or other source URL. |

| `created\_at` | datetime | Timestamp when record was created. |



\---



\# Table: `sale\_outcomes`



Future table for comparing model predictions with final sale prices.



| Field Name | Type | Description |

|---|---:|---|

| `sale\_outcome\_id` | string | Unique sale outcome record ID. |

| `property\_id` | string | Internal property ID. |

| `original\_list\_price` | integer | First observed listing price. |

| `last\_list\_price\_before\_contract` | integer | Last observed list price before under contract/pending. |

| `final\_sale\_price` | integer | Confirmed final sale price. |

| `sale\_date` | date | Confirmed sale date. |

| `estimated\_fair\_value\_at\_prediction` | float | Frozen fair value estimate from before sale. |

| `sale\_price\_vs\_estimated\_fair\_value\_pct` | float | Prediction error relative to fair value estimate. |

| `absolute\_prediction\_error\_pct` | float | Absolute percent error. |

| `model\_version\_used` | string | Model version that generated the estimate. |

| `outcome\_notes` | string | Notes about confidence and source. |



\---



\# Field Trust Levels



\## Trusted for MVP if present



\- address

\- city

\- state

\- zip\_code

\- latitude

\- longitude

\- home\_type

\- price

\- beds

\- baths

\- square\_feet

\- zillow\_url



\## Useful but requires caution



\- zestimate

\- rent\_zestimate

\- lot\_size

\- days\_on\_zillow

\- price cuts

\- listing description

\- year built

\- HOA fees

\- property taxes



\## Do not use for serious scoring until validated



\- estimated fair value

\- comparable-sale estimate

\- cap rate

\- cash-on-cash return

\- final sale price

\- sold outcome metrics

\- condition risk from listing text



\---



\# Update Rules



This document should be updated after each major data inspection.



For each field, add:



\- actual source path in raw Zillow output

\- percent missing

\- cleaning rule

\- whether field is safe for MVP

\- whether field needs manual validation

