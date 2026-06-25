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

