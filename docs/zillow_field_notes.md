\# Zillow Field Notes



\## Purpose



This document tracks what fields are actually available from the Zillow connector and how reliable those fields appear to be.



The goal is to avoid designing the project around fields that may not exist, may be missing often, or may require manual validation.



This document should be updated after each Zillow connector pull.



\---



\## Current Status



The MVP pipeline is complete. Multiple raw Zillow connector pulls have been

saved and logged below (Search Pulls 1-7, Detail Probes 1-6), most recently

the active-listing candidate refresh on 2026-07-04. The 2026-06-24 sample at

`data/raw/zillow_raw_search_20260624.json` has been normalized end-to-end

through `outputs/reports/mvp_run_summary.md`.



This document is a running log, not a planning template. Continue updating

it after each new connector pull per the Update Rules section below.



\---



\# Field Availability Log

## Search Pull 1


| Item | Value |
|---|---|
| Pull date | 2026-06-24 |
| Search area | ZIP code 02131 |
| Search radius | ZIP-only demo search; full 25-mile radius later |
| Property types requested | single-family, condo, townhome, multifamily |
| Listing statuses requested | for sale by agent, for sale by owner, coming soon, new construction |
| Number of records returned | 50 |
| Raw file path | Not yet saved locally |
| Notes | First connector pull showed search-level fields only. Zestimate, Rent Zestimate, listing description, days on market, price history, tax history, and sale history were not returned in the basic search output. These may require property-detail pulls. |

## Fields observed in Search Pull 1

| Field | Observed? | Notes |
|---|---:|---|
| `formattedAddress.line1` | Yes | Street address or unit address. One listing had undisclosed address. |
| `formattedAddress.line2` | Yes | City/state/ZIP line. |
| `formattedAddress.city` | Yes | Values included Roslindale and Boston. |
| `formattedAddress.stateOrProvince` | Yes | MA. |
| `formattedAddress.postalCode` | Yes | 02131. |
| `geoRegion.latLong.latitude` | Mostly yes | One undisclosed-address record lacked lat/long. |
| `geoRegion.latLong.longitude` | Mostly yes | Needed for distance calculations. |
| `geoRegion.isBadGeocode` | Yes | Returned false in observed records. |
| `bathroomCount` | Yes | Numeric. |
| `bedroomCount` | Yes | Numeric. |
| `livingAreaSquareFeet` | Yes | Numeric. |
| `lotArea.size` | Sometimes | Missing for some condos/units. |
| `lotArea.sizeUnits` | Sometimes | Observed Square Feet and Acres. |
| `fixtureClassification` | Yes | Observed improvement, unit, representative. |
| `homeType` | Yes | Observed singleFamily, condo, townhome, multiFamily. |
| `title` | Sometimes | Often condo/community name. |
| `price.filteredPrice` | Yes | Listing price. |
| `newConstruction.availablePlanCnt` | Yes | Numeric. |
| `newConstruction.premierBuilder` | Yes | Boolean. |
| `hasOpenHouse` | Yes | Boolean. |
| `hasVRModel` | Yes | Boolean. |
| `homeDetailsPageUrl` | Yes | Zillow URL. |
| `zestimate` | No | Not returned in basic search output. |
| `rent_zestimate` | No | Not returned in basic search output. |
| `days_on_zillow` | No | Not returned in basic search output. |
| `listing_description` | No | Not returned in basic search output. |
| `price_history` | No | Not returned in basic search output. |
| `tax_history` | No | Not returned in basic search output. |
| `sale_history` | No | Not returned in basic search output. |

## Immediate MVP implications

---

# Detail Probe 1 — Zestimate and Rent Zestimate

## Probe date

2026-06-25

## Property tested

41 Brown Ave, Roslindale, MA 02131

## Purpose

Test whether Zillow connector can return Zestimate and Rent Zestimate through separate detail-style calls, because those fields were not returned in the basic search-level output.

## Result

The Zillow connector returned both:

- Zestimate
- Rent Zestimate

## Zestimate result

```text
The Zestimate for 41 Brown Ave Roslindale, MA 02131 is $1,606,400 ($515/sqft) with the estimated sales range of $1,526,000 - $1,687,000.
The listing price, set by the seller, is a key input to the Zestimate for this property.

The first normalized dataframe should focus on:

- address
- city
- state
- zip code
- latitude
- longitude
- price
- beds
- baths
- square feet
- lot size
- lot size units
- home type
- fixture classification
- new construction flag
- open house flag
- VR model flag
- Zillow URL
- search date
- data source

Do not build scoring yet.

Next technical step should be creating a simple raw sample file and then a normalization script that extracts the observed search-level fields.
\## Search Pull 1

---

# Detail Probe 2 — Multi-Property Zestimate and Rent Zestimate Validation

## Probe date

2026-06-25

## Purpose

Test whether Zestimate and Rent Zestimate are available across different property types, not just one single-family property.

The first search-level Zillow connector output did not return Zestimate or Rent Zestimate directly. This probe tests whether those fields can be retrieved through separate Zillow valuation calls.

## Properties tested

| Property | Property type | Zestimate returned? | Rent Zestimate returned? | Notes |
|---|---|---:|---:|---|
| 41 Brown Ave, Roslindale, MA 02131 | Single-family | Yes | Yes | First detail probe. |
| 15 S Fairview St #3, Roslindale, MA 02131 | Condo | Yes | Yes | Zestimate call returned comps and noted seller listing price as key input. |
| 45 Harrison St APT B, Roslindale, MA 02131 | Townhouse | Yes | Yes | Zestimate call returned comps and noted seller listing price as key input. |
| 74-76 Poplar St, Roslindale, MA 02131 | Multifamily | Yes | Yes | Zestimate call returned comps and noted seller listing price as key input. |

## Values returned

| Property | Zestimate | Zestimate per sqft | Estimated sales range | Rent Zestimate |
|---|---:|---:|---|---:|
| 41 Brown Ave | $1,606,400 | $515/sqft | $1,526,000 - $1,687,000 | $5,023 |
| 15 S Fairview St #3 | $579,600 | $393/sqft | $551,000 - $609,000 | $3,488 |
| 45 Harrison St APT B | $595,500 | $344/sqft | $566,000 - $625,000 | $3,834 |
| 74-76 Poplar St | $1,178,500 | $304/sqft | $1,120,000 - $1,237,000 | $4,338 |

## Confirmed available through separate detail calls

| Field | Availability after probe | Use status |
|---|---|---|
| Zestimate | Available for 4/4 tested properties | Useful but cautious |
| Zestimate per square foot | Available for 4/4 tested properties | Useful but cautious |
| Estimated sales range | Available for 4/4 tested properties | Useful but cautious |
| Rent Zestimate | Available for 4/4 tested properties | Useful but cautious |
| Comparable homes | Available for 4/4 tested properties | Requires parsing and validation |
| Comp sale prices | Available for 4/4 tested properties | Requires parsing and validation |
| Comp sale timing | Available for 4/4 tested properties | Requires parsing and validation |
| Comp Zestimate | Available for 4/4 tested properties | Requires parsing and validation |

## Important caution

For all tested properties, Zillow stated that the seller listing price is a key input to the Zestimate.

This means Zestimate should not be treated as an independent estimate of fair value for active listings. It may partly reflect the asking price.

## Pipeline implication

The project should use a two-stage data collection approach:

1. Use search-level pulls to identify and normalize candidate properties.
2. Use detail/valuation calls only on selected properties to retrieve Zestimate, Rent Zestimate, sales range, and comparable-home text.

## Scoring implication

Do not use Zestimate as the dominant valuation signal.

Potential future use:

- price vs Zestimate as a weak/moderate signal
- Zestimate sales range as a confidence/context field
- Rent Zestimate for rough gross-rent-yield screening
- comparable-sale text as a future parsing target

Do not build final scoring until these fields are tested on a larger and more diverse sample.


| Item | Value |

|---|---|

| Pull date | TBD |

| Search area | 02131 demo search |

| Search radius | Initial demo; full 25-mile radius later |

| Property types requested | single-family, condo, townhome, multifamily |

| Number of records returned | TBD |

| Raw file path | `data/raw/zillow\_raw\_search\_YYYYMMDD.json` |

| Notes | TBD |

---

# Search Pull 3 — Price-Reduction Filter Probe

## Pull date

2026-06-26

## Purpose

Test whether the Zillow connector can return a subset of active residential properties with price reductions inside the approximate 25-mile search area around ZIP code 02131.

This pull is for signal validation only.

Do not score properties yet.

## Search setup

| Item | Value |
|---|---|
| Center area | ZIP code 02131 |
| Search type | Approximate 25-mile polygon around 02131 |
| Property statuses | for sale by agent, for sale by owner, coming soon, new construction |
| Property types | single-family, condo, townhome, multifamily |
| Additional filter | price reduction |
| Total matching count | 2,093 |
| Displayed result count | 100 |

## Fields returned

The price-reduction pull returned the same basic search-level fields as prior search pulls:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- listing price
- title, sometimes
- new construction flags
- open house flag
- VR model flag
- Zillow detail URL

## Important finding

The price-reduction filter works as a search filter, but the returned structured fields did not clearly include:

- previous list price
- price cut amount
- price cut percentage
- price cut date
- days on market

This means price reduction can be used as a candidate-selection flag, but the actual price-cut details may require a property-detail pull or manual validation.

## MVP implication

Future pipeline field to add:

- `zillow_price_reduction_filter_match`

This field should mean:

The property appeared in a Zillow connector search that was filtered for price reductions.

It should not mean we know the exact price-cut amount or date.

## Scoring implication

Do not score price reductions yet.

Possible future use:

- weak positive signal if property appears in price-reduction search
- stronger signal only if prior price, current price, cut amount, and cut date are confirmed
- reduce confidence if price-cut details are missing

## Required validation before scoring

Before using price cuts in the scoring model, validate whether detail-level Zillow calls can return:

- previous price
- current price
- price history
- date of price reduction
- size of price reduction
- number of price cuts


---

# Detail Probe 3 — Active Price-Reduction Listing Detail Test

## Probe date

2026-06-26

## Purpose

Test whether Zillow property-detail calls can return price-history or price-cut details for active listings that appeared in the price-reduction search.

## Properties tested

| Property | Listing context | Detail call result |
|---|---|---|
| 15 S Fairview St #3, Roslindale, MA 02131 | Active price-reduction candidate | Failed. Zillow reported active/Showcase listing details are not supported. |
| 45 Bonair St, West Roxbury, MA 02132 | Active price-reduction candidate | Failed. Zillow reported active for-sale listing details are not supported. |
| 249 Mill St, Randolph, MA 02368 | Active price-reduction candidate | Failed. Zillow reported active for-sale listing details are not supported. |

## Finding

The Zillow connector can return active listings through search, including a price-reduction-filtered search.

However, the property-detail tool did not return full active-listing details for the tested active listings.

The detail tool reported that only off-market properties are currently supported.

## Fields still not validated for active listings

The following fields remain unavailable or unvalidated for active listings:

- previous list price
- price cut amount
- price cut percentage
- price cut date
- full price history
- days on Zillow
- listing description
- tax history
- sale history
- HOA fee
- property tax
- listing-agent details

## MVP implication

For active listings, use the search-level fields as the reliable MVP base.

The price-reduction search should create only this field:

- `zillow_price_reduction_filter_match`

This means the property appeared in a search filtered for price reductions.

It does not mean the exact price-cut amount, date, or prior list price is known.

## Scoring implication

Do not score price-cut magnitude yet.

Possible future scoring use:

- weak positive signal: appeared in price-reduction search
- stronger signal only if price-history fields become available
- confidence penalty if price-reduction details are missing

## Decision

Do not build price-history scoring yet.

Next recommended technical step:

Build geography validation in `src/geocoding.py`, because latitude and longitude are available from search-level output and the 25-mile radius rule is a hard project filter.

\---



\# Expected Fields to Inspect



\## Property identity



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| zpid | Yes | TBD | TBD | Best unique property identifier if available. |

| address | Yes | TBD | TBD | May be partial or undisclosed. |

| zillow\_url | Yes | TBD | TBD | Needed for manual review. |



\## Location



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| city | Yes | TBD | TBD | Needed for grouping and filtering. |

| state | Yes | TBD | TBD | Should be MA. |

| zip\_code | Yes | TBD | TBD | Store as text. |

| latitude | Yes | TBD | TBD | Needed for distance calculation. |

| longitude | Yes | TBD | TBD | Needed for distance calculation. |



\## Listing status



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| home\_status | Yes | TBD | TBD | For sale, pending, sold, etc. |

| status\_text | Maybe | TBD | TBD | Useful for lifecycle tracking. |

| days\_on\_zillow | Maybe | TBD | TBD | Useful but may be missing. |



\## Price and valuation



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| price | Yes | TBD | TBD | Required for MVP. |

| zestimate | Maybe | TBD | TBD | Useful but not ground truth. |

| rent\_zestimate | Maybe | TBD | TBD | Useful for income screen if available. |

| price\_history | Maybe | TBD | TBD | Likely requires property detail pull. |

| tax\_history | Maybe | TBD | TBD | Likely requires property detail pull or outside source. |

| sale\_history | Maybe | TBD | TBD | Requires validation. |



\## Property characteristics



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| home\_type | Yes | TBD | TBD | Single-family, condo, townhome, multifamily. |

| beds | Yes | TBD | TBD | Core field. |

| baths | Yes | TBD | TBD | Core field. |

| square\_feet | Yes | TBD | TBD | Core valuation field. |

| lot\_size | Maybe | TBD | TBD | Units must be checked. |

| year\_built | Maybe | TBD | TBD | Useful if available. |

| hoa\_fee | Maybe | TBD | TBD | Important for condos; likely incomplete. |

| property\_tax | Maybe | TBD | TBD | Must validate. |



\## Listing text



| Field | Expected? | Actual source path | Availability | Notes |

|---|---:|---|---|---|

| listing\_description | Maybe | TBD | TBD | Use conservatively. |

| listing\_agent | Maybe | TBD | TBD | Not core for MVP. |

| brokerage | Maybe | TBD | TBD | Not core for MVP. |



\---



\# Field Trust Levels



\## Likely safe for MVP if present



\- zpid

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

\- days\_on\_zillow

\- lot\_size

\- year\_built

\- price cuts

\- listing description

\- HOA fees

\- property taxes



\## Do not trust without validation



\- final sale price

\- cap rate

\- cash-on-cash return

\- fair value estimate

\- comparable-sales estimate

\- condition quality inferred from listing text



\---



\# Known Risks



\## Search geography risk



Zillow search areas may not perfectly match a 25-mile radius around 02131.



Solution:



\- Pull listings by ZIP/city/area.

\- Use latitude and longitude when available.

\- Calculate distance from 02131 manually in Python.

\- Flag properties outside the target radius.



\## Duplicate listing risk



The same property may appear multiple times.



Possible duplicate keys:



\- same zpid

\- same address

\- same latitude/longitude

\- same address plus price



\## Missing field risk



Important fields may be missing, especially:



\- Zestimate

\- Rent Zestimate

\- HOA fee

\- tax data

\- sale history

\- listing description

\- days on market



Missing fields should reduce confidence, not create false opportunity signals.



\## Stale listing risk



A listing may be old, off market, pending, or otherwise stale.



The pipeline should flag unclear listing statuses instead of assuming the property is active.



\---



\# Update Rules



After every raw Zillow connector pull, update this document with:



1\. Search date

2\. Search query used

3\. Number of records returned

4\. Raw file path

5\. Actual field names

6\. Actual nested source paths

7\. Percent missing by field

8\. Notes on duplicates or odd records

9\. Fields safe for MVP

10\. Fields not safe for MVP

---

# Search Pull 4 — Recently Sold / Sale Outcome Probe

## Pull date

2026-06-29

## Purpose

Test whether the Zillow connector can return recently sold residential properties inside the approximate 25-mile search area around ZIP code 02131.

This pull is for lifecycle-tracking and future model-backtesting validation only.

Do not score properties yet.

## Search setup

| Item | Value |
|---|---|
| Center area | ZIP code 02131 |
| Search type | Approximate 25-mile polygon around 02131 |
| Property status | recently sold |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 98,501 |
| Displayed result count | 100 |

## Fields returned

The recently sold search returned the same basic search-level fields as prior searches:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- filtered price
- title, sometimes
- new construction flags
- open house flag
- VR model flag
- Zillow detail URL

## Important finding

The Zillow connector can return a recently sold search universe.

However, the search-level output did not clearly return structured fields for:

- sale date
- original list price
- last list price before sale
- days on market
- status change date
- confirmed sale price flag
- price change history

## MVP implication

Future pipeline field to add:

- `zillow_recently_sold_filter_match`

This field should mean:

The property appeared in a Zillow connector search filtered for recently sold properties.

It should not yet mean that the project has a fully validated final sale outcome.

## Sale-outcome implication

The `price.filteredPrice` field in a recently sold search may represent a sold price, but this needs validation before it is used for model backtesting.

Do not treat it as a confirmed final sale price until we test recently sold property details or compare against another reliable source.

## Required validation before backtesting

Before using recently sold data for model evaluation, validate whether Zillow or another source can return:

- final sale price
- sale date
- prior list price
- price history
- days on market
- property status history
- whether the sale price is confirmed

## Decision

Do not build sale-outcome backtesting yet.

Use this pull only to confirm that a recently sold search universe exists.

Next technical step should remain local pipeline strengthening before scoring or backtesting.


---

# Search Pull 4B — Recently Sold Widget-State Field Audit

## Pull date

2026-06-29

## Purpose

Review the enhanced Zillow widget-state fields returned from the recently sold search.

This is a follow-up to Search Pull 4.

The goal is to determine whether recently sold results expose enough structured data to support future sale-outcome tracking.

Do not build backtesting yet.

## Important finding

The basic search response returned search-level fields such as address, city, state, ZIP code, latitude, longitude, beds, baths, square feet, home type, price, and Zillow URL.

However, the Zillow widget state also exposed additional useful fields for many recently sold records.

## Additional fields observed in widget state

| Field | Observed? | Notes |
|---|---:|---|
| `zpid` | Yes | Strong candidate for property identifier. |
| `statusType` | Yes | Observed `SOLD` in widget state. |
| `statusText` | Yes | Observed `Sold`. |
| `price` | Yes | Display-formatted sale/list price, sometimes `$650,000`, sometimes `1.2M`. |
| `priceLabel` | Yes | Short formatted price label, such as `$650K`. |
| `countryCurrency` | Yes | Observed `usd`. |
| `address` | Yes | Full display address, sometimes with duplicated ZIP. |
| `beds` | Yes | Bedroom count. |
| `baths` | Yes | Bathroom count. |
| `area` | Yes | Living area square feet. |
| `latLong.latitude` | Yes | Required for distance validation. |
| `latLong.longitude` | Yes | Required for distance validation. |
| `hdpData.homeInfo.homeStatus` | Yes | Often `RECENTLY_SOLD`, but one observed case conflicted with top-level sold status. |
| `hdpData.homeInfo.homeType` | Yes | Observed `SINGLE_FAMILY`, `CONDO`, `TOWNHOUSE`, `MULTI_FAMILY`. |
| `hdpData.homeInfo.zestimate` | Often | Available for many sold properties, but missing for some. |
| `hdpData.homeInfo.rentZestimate` | Often | Available for many sold properties, but missing for some. |
| `buildingName` | Sometimes | Mostly condos/townhomes. |
| `lotId` | Sometimes | Mostly condos/townhomes or buildings. |

## Status consistency issue

At least one recently sold widget record showed a possible inconsistency:

- top-level `statusType`: `SOLD`
- top-level `statusText`: `Sold`
- nested `hdpData.homeInfo.homeStatus`: `FOR_SALE`

This means future lifecycle logic should not trust a single status field blindly.

## MVP implication

For recently sold records, create future fields such as:

- `zillow_recently_sold_filter_match`
- `sold_search_status_type`
- `sold_search_status_text`
- `nested_home_status`
- `status_conflict_flag`
- `sold_search_price`
- `sold_search_price_label`
- `sold_search_zestimate`
- `sold_search_rent_zestimate`

## Sale-outcome caution

The recently sold widget state makes sale-outcome tracking more realistic, but it still does not fully validate:

- exact sale date
- original list price
- last list price before sale
- price history
- days on market
- whether `price` is confirmed final sale price
- whether the record represents a clean resale, new construction, unit sale, or other transaction type

## Future validation rule

Before backtesting, require one of the following:

1. A confirmed sale date and final sale price from Zillow detail or another reliable source.
2. A manual validation flag confirming that the sold search price is the final sale price.
3. A secondary public-record check.

## Decision

Do not build model backtesting yet.

However, the recently sold widget state is strong enough to justify creating a structured `recently_sold_probe_results.csv` in a future coding phase.

Next recommended coding phase:

Create a small manually entered recently sold probe table with:

- zpid
- address
- sold_search_price
- statusType
- statusText
- nested_home_status
- zestimate
- rent_zestimate
- beds
- baths
- square_feet
- latitude
- longitude
- status_conflict_flag
- sale_outcome_needs_validation

---

# Detail Probe 4 — Recently Sold Detail Validation

## Probe date

2026-06-29

## Purpose

Test whether Zillow property-detail calls can return richer sale-outcome fields for recently sold properties.

This follows Search Pull 4 and Search Pull 4B.

The goal is to determine whether recently sold properties can support future sale-outcome tracking and model backtesting.

Do not build backtesting yet.

## Properties tested

| Property | Property type/context | Detail call result |
|---|---|---|
| 11 Eugenia Rd, Roslindale, MA 02131 | Recently sold single-family candidate | Detail call succeeded. Returned tax/geography/parcel fields, but not clean sale date or final sale price. |
| 114 Curve St, Dedham, MA 02026 | Recently sold single-family candidate | Detail call succeeded. Returned tax/geography/parcel fields, but not clean sale date or final sale price. |
| 56 School St, Somerville, MA 02143 | Recently sold multifamily candidate | Detail call succeeded. Returned tax/geography/parcel fields, but not clean sale date or final sale price. |

## Fields returned by recently sold detail calls

The detail payload returned fields including:

- address
- city
- state
- ZIP code
- latitude
- longitude
- parcel ID
- county
- county FIPS
- tax assessed value
- tax assessed year
- property tax rate
- tax history
- foreclosure flags
- undisclosed-address flag
- non-owner-occupied flag
- timezone
- static map / street view references

## Fields not clearly returned

The detail payload did not clearly return structured fields for:

- confirmed final sale price
- sale date
- original list price
- last list price before sale
- days on market
- price history
- sale history
- beds
- baths
- square feet
- listing description

## Important finding

Recently sold detail calls are useful for tax and parcel enrichment.

However, they are not sufficient by themselves for model backtesting because final sale date and confirmed final sale price were not clearly returned in the tested detail payloads.

## MVP implication

Recently sold detail calls can support future enrichment fields such as:

- `tax_assessed_value`
- `tax_assessed_year`
- `property_tax_rate`
- `parcel_id`
- `county`
- `county_fips`
- `tax_history_available`
- `foreclosure_flag_available`
- `is_undisclosed_address`
- `is_non_owner_occupied`

## Backtesting implication

Do not use the recently sold detail payload alone to calculate model accuracy.

Backtesting still requires validated sale-outcome fields:

- final sale price
- sale date
- model estimate frozen before sale
- model version
- original list price
- last list price before sale

## Decision

Do not build model backtesting yet.

The next safe coding step is to add a structured recently sold detail-probe table that records which tax/parcel fields are available and flags sale-outcome fields as unavailable or needing validation.


---

# Detail Probe 5 — Recently Sold Zestimate-History Validation

## Probe date

2026-06-29

## Purpose

Test whether Zillow can return Zestimate-history data for recently sold or off-market properties.

This follows the recently sold search probe and recently sold detail validation.

The goal is to determine whether Zestimate history can support valuation-trend context for future research notes.

Do not build backtesting yet.

## Properties tested

| Property | Zestimate history returned? | Current Zestimate | History range returned |
|---|---:|---:|---|
| 11 Eugenia Rd, Roslindale, MA 02131 | Yes | $834,900 | 2021-06-30 through 2026-05-31 |
| 114 Curve St, Dedham, MA 02026 | Yes | $808,900 | 2021-06-30 through 2026-05-31 |
| 56 School St, Somerville, MA 02143 | Yes | $1,610,200 | 2023-06-30 through 2026-05-31 |

## Fields returned

The Zestimate-history tool returned:

- address
- current Zestimate
- monthly percentage-change history
- Zestimate disclaimer

## Fields not returned

The Zestimate-history tool did not return:

- final sale price
- sale date
- original list price
- last list price before sale
- price history
- tax history
- beds
- baths
- square feet
- listing description

## Important caution

Zillow states that the Zestimate is Zillow's estimate of a home's market value. It incorporates public, MLS, and user-submitted data, including listing information, sale prices, tax assessor data, home facts, location, and market trends. It is not an appraisal and should not be used as a substitute for one.

This means Zestimate history can be used as context, but not as ground truth.

## MVP implication

Future table fields to add:

- `current_zestimate`
- `zestimate_history_available`
- `zestimate_history_start_date`
- `zestimate_history_end_date`
- `zestimate_pct_change_latest`
- `zestimate_pct_change_min`
- `zestimate_pct_change_max`
- `zestimate_pct_change_volatility`

## Scoring implication

Do not use Zestimate history as a dominant score driver.

Potential future uses:

- valuation-trend context
- confidence/context field in property research notes
- warning flag if Zestimate moved sharply near the sale/search date
- comparison against listing price only after data-quality checks

## Backtesting implication

Zestimate history does not solve sale-outcome validation.

Backtesting still requires:

- confirmed final sale price
- sale date
- model estimate frozen before sale
- model version used at scoring time

## Decision

Do not build model backtesting yet.

The next safe coding step is to create a structured recently sold detail/history probe table that records tax/parcel fields and Zestimate-history availability while keeping sale-outcome fields marked as unconfirmed.

---

# Detail Probe 6 — Recently Sold Rent Zestimate Validation

## Probe date

2026-06-29

## Purpose

Test whether Zillow can return Rent Zestimate values for recently sold or off-market properties.

This follows the recently sold search probe, detail validation, and Zestimate-history validation.

The goal is to determine whether Rent Zestimate can support income-context fields in future research notes and enrichment tables.

Do not build scoring or backtesting yet.

## Properties tested

| Property | Rent Zestimate returned? | Rent Zestimate |
|---|---:|---:|
| 11 Eugenia Rd, Roslindale, MA 02131 | Yes | $3,294 |
| 114 Curve St, Dedham, MA 02026 | Yes | $4,123 |
| 56 School St, Somerville, MA 02143 | Yes | $4,784 |

## Fields returned

The Rent Zestimate tool returned:

- address
- Rent Zestimate value
- Zillow Zestimate disclaimer text

## Fields not returned

The Rent Zestimate tool did not return:

- rent range
- rent history
- unit-level rent breakdown
- vacancy assumptions
- expense assumptions
- confirmed lease data
- final sale price
- sale date

## Important caution

Zillow states that the Zestimate is Zillow's estimate of a home's market value. It incorporates public, MLS, and user-submitted data, including listing information, sale prices, tax assessor data, home facts, location, and market trends. It is not an appraisal and should not be used as a substitute for one.

Rent Zestimate should be treated as a rough income-context signal, not confirmed market rent.

## MVP implication

Future table fields to add:

- `rent_zestimate_available`
- `rent_zestimate`
- `annual_rent_zestimate`
- `gross_rent_yield_using_sold_search_price`
- `rent_zestimate_needs_validation`

## Scoring implication

Do not use Rent Zestimate as a dominant score driver yet.

Potential future uses:

- rough income-context field
- gross-rent-yield screen
- multifamily income-context review
- research-note prompt input

## Backtesting implication

Rent Zestimate does not solve sale-outcome validation.

Backtesting still requires:

- confirmed final sale price
- sale date
- model estimate frozen before sale
- model version used at scoring time

## Decision

Do not build model backtesting yet.

The next safe coding step is to create a structured recently sold enrichment probe table that combines:

- recently sold search fields
- tax / parcel detail availability
- Zestimate-history availability
- Rent Zestimate availability
- sale-outcome validation flags


---

# Search Pull 5 — Recently Sold Comparable-Universe Probe

## Pull date

2026-07-01

## Purpose

Test whether the Zillow connector can return a local recently sold universe around Roslindale / ZIP code 02131 that may later support comparable-sales context.

This is not a valuation model yet.

Do not build scoring or backtesting yet.

## Search setup

| Item | Value |
|---|---|
| Search area | Roslindale, Boston, MA / ZIP 02131 |
| Property status | Recently sold |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 728 |
| Displayed result count | 100 |

## Fields returned

The recently sold comparable-universe search returned:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- sold-search price
- title, sometimes
- new construction flags
- open house flag
- VR model flag
- Zillow detail URL

## Example records returned

| Property | Type | Sold-search price | Beds | Baths | Sqft |
|---|---|---:|---:|---:|---:|
| 41 Mount Hope St, Roslindale, MA 02131 | single-family | $640,000 | 3 | 1 | 1,616 |
| 951 Canterbury St, Roslindale, MA 02131 | multifamily | $775,000 | 4 | 3 | 2,446 |
| 52 Walter St, Roslindale, MA 02131 | single-family | $1,200,000 | 3 | 3 | 1,868 |
| 11 Eugenia Rd, Roslindale, MA 02131 | single-family | $927,000 | 2 | 2 | 1,750 |
| 41 Cornell St, Roslindale, MA 02131 | single-family | $980,000 | 3 | 2 | 1,720 |
| 602 Canterbury St #6, Roslindale, MA 02131 | townhome | $505,154 | 2 | 2 | 1,251 |
| 63 Bradwood St, Roslindale, MA 02131 | multifamily | $1,200,000 | 5 | 3 | 3,388 |
| 209 Beech St, Roslindale, MA 02131 | single-family | $1,300,000 | 3 | 3 | 2,534 |
| 122 Aldrich St, Roslindale, MA 02131 | multifamily | $1,015,000 | 7 | 2 | 2,616 |
| 36 Orange St, Roslindale, MA 02131 | single-family | $1,250,000 | 4 | 3 | 2,524 |

## Important finding

The Zillow connector can return a local recently sold universe that may later support comparable-sales context.

However, this search does not yet provide a true comp model.

The returned records do not clearly include:

- confirmed sale date
- original list price
- last list price before sale
- days on market
- price history
- condition details
- renovation status
- sale concessions
- true comp similarity score
- manual property adjustments

## MVP implication

Future field to add:

- `zillow_recently_sold_comp_universe_match`

This field should mean:

The property appeared in a recently sold search for the target local area.

It should not mean the property is automatically a valid comparable sale.

## Future comp-table implication

A future comparable-sales table should include:

- subject_property_id
- comp_property_id
- comp_address
- comp_city
- comp_zip_code
- comp_home_type
- comp_sold_search_price
- comp_beds
- comp_baths
- comp_square_feet
- comp_price_per_sqft
- comp_latitude
- comp_longitude
- comp_distance_from_subject_miles
- comp_distance_from_02131_miles
- comp_sale_date_available
- comp_final_sale_price_confirmed
- comp_similarity_needs_validation
- comp_exclusion_reason

## Decision

Do not build a comp valuation model yet.

This probe supports a future comparable-sales universe, but comp selection still requires stricter filters by property type, size, distance, sale date, and data quality.



---

# Search Pull 6 — Recently Sold Comparable-Universe Refresh

## Pull date

2026-07-02

## Purpose

Refresh the recently sold residential search for Roslindale / ZIP code 02131 after the recently sold enrichment-table phase.

This tests whether Zillow can still return a local recently sold universe for future comparable-sales context.

This is not a valuation model.

Do not build scoring or backtesting yet.

## Search setup

| Item | Value |
|---|---|
| Search area | Roslindale / ZIP 02131 |
| Property status | Recently sold |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 792 |
| Displayed result count | 100 |

## Fields returned in search response

The recently sold search returned these search-level fields:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- sold-search price
- title, sometimes
- new construction flags
- open house flag
- VR model flag
- Zillow detail URL

## Additional fields visible in widget state

The Zillow widget state also exposed additional useful fields for many records:

- `zpid`
- `statusType`
- `statusText`
- `price`
- `priceLabel`
- `countryCurrency`
- `buildingName`, sometimes
- `lotId`, sometimes
- `hdpData.homeInfo.homeStatus`
- `hdpData.homeInfo.homeType`
- `hdpData.homeInfo.zestimate`, sometimes
- `hdpData.homeInfo.rentZestimate`, often

These fields are useful for local enrichment tables, but they still need validation before scoring.

## Example records returned

| Property | Type | Sold-search price | Beds | Baths | Sqft | Zestimate in widget? | Rent Zestimate in widget? |
|---|---|---:|---:|---:|---:|---:|---:|
| 214 Florence St #1A, Roslindale, MA 02131 | townhome | $475,000 | 3 | 2 | 1,074 | No | No |
| 21 Stella Rd, Roslindale, MA 02131 | single-family | $640,000 | 2 | 2 | 1,066 | Yes | Yes |
| 338 Beech St, Roslindale, MA 02131 | single-family | $1,162,000 | 3 | 3 | 1,800 | Yes | Yes |
| 41 Mount Hope St, Roslindale, MA 02131 | single-family | $640,000 | 3 | 1 | 1,616 | Yes | Yes |
| 951 Canterbury St, Roslindale, MA 02131 | multifamily | $775,000 | 4 | 3 | 2,446 | Yes | Yes |
| 52 Walter St, Roslindale, MA 02131 | single-family | $1,200,000 | 3 | 3 | 1,868 | No | Yes |
| 11 Eugenia Rd, Roslindale, MA 02131 | single-family | $927,000 | 2 | 2 | 1,750 | Yes | Yes |
| 41 Cornell St, Roslindale, MA 02131 | single-family | $980,000 | 3 | 2 | 1,720 | Yes | Yes |
| 602 Canterbury St #6, Roslindale, MA 02131 | townhome | $505,154 | 2 | 2 | 1,251 | Yes | Yes |
| 63 Bradwood St, Roslindale, MA 02131 | multifamily | $1,200,000 | 5 | 3 | 3,388 | No | Yes |

## Important finding

The recently sold universe changed materially from the prior comparable-universe probe.

Prior comparable-universe probe:

- total matching count: 728
- displayed result count: 100

Current refresh:

- total matching count: 792
- displayed result count: 100

This confirms that Zillow recently sold search results can change over time.

## MVP implication

Future local tables should preserve:

- `connector_pull_date`
- `search_area`
- `search_status`
- `property_types_requested`
- `total_matching_count`
- `displayed_result_count`
- `zillow_recently_sold_comp_universe_match`
- `sold_search_price_needs_validation`
- `zestimate_from_widget_available`
- `rent_zestimate_from_widget_available`

## Sale-outcome caution

The sold-search price should not be treated as a confirmed final sale price unless independently validated.

This search still does not clearly provide:

- confirmed sale date
- confirmed final sale price
- original list price
- last list price before sale
- days on market
- full price history
- condition details
- true comparable-sale similarity score

## Decision

Use this pull as a fresh recently sold comp-universe refresh.

Do not build a comp valuation model yet.

Do not build scoring yet.

Do not build backtesting yet.

Next safe local coding step:

Create a recently sold comp-universe sample table that stores selected search-level and widget-state fields from this pull and includes conservative validation flags.

---

# Local Table 4 — Recently Sold Comp-Universe Sample Table

## Table creation date

2026-07-02

## Related phase

Phase 12J / Phase 12K

## Purpose

Create a local CSV sample of recently sold Roslindale / ZIP 02131 properties returned by the Zillow connector.

This table preserves a small representative sample of search-level recently sold records so the project can later develop comparable-sales context.

This is not a valuation model.

This is not a backtesting dataset.

This does not confirm sale dates or final sale prices.

## Input source

Zillow connector recently sold search:

| Item | Value |
|---|---|
| Search area | Roslindale / ZIP 02131 |
| Property status | Recently sold |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 792 |
| Displayed result count | 100 |

## Script

```text
scripts/create_recently_sold_comp_universe_sample_table.py



---

# Search Pull 7 — Active Listing Candidate Refresh

## Pull date

2026-07-03

## Related phase

Phase 13A / Phase 13B

## Purpose

Refresh active residential listings in Roslindale / ZIP 02131 and use the result as the source context for the active-listing candidate table.

This pull supports the first active candidate-review table.

This is not a valuation model.

This is not a scoring phase.

This is not a buy/sell recommendation.

## Search setup

| Item | Value |
|---|---|
| Search area | Roslindale / ZIP 02131 |
| Property status | Active for-sale listings |
| Listing statuses | active, coming soon, Zillow Preview |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 41 |
| Displayed result count | 41 |

## Fields returned in search response

The active listing search returned these search-level fields:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- listing price
- title, sometimes
- new construction available plan count
- new construction premier builder flag
- open house flag
- VR model flag
- Zillow detail URL

## Additional fields visible in widget state

The Zillow widget state also exposed additional useful fields for many active records:

- `zpid`
- `statusType`
- `statusText`
- `price`
- `priceLabel`
- `countryCurrency`
- `buildingName`, sometimes
- `lotId`, sometimes
- `plid`, sometimes
- `hdpData.homeInfo.homeStatus`
- `hdpData.homeInfo.homeType`
- `hdpData.homeInfo.zestimate`, sometimes
- `hdpData.homeInfo.rentZestimate`, sometimes
- `isUndisclosedAddress`, sometimes

These fields may be useful for future enrichment, but the normalized Phase 13A candidate table should still treat the record as search-level evidence unless detail validation is completed.

## Example active records returned

| Property | Type | Listing price | Beds | Baths | Sqft | Widget Zestimate? | Widget Rent Zestimate? |
|---|---|---:|---:|---:|---:|---:|---:|
| 602 Canterbury St #10U, Roslindale, MA 02131 | townhome | $515,000 | 2 | 2 | 1,251 | No | No |
| 11 Whipple Ave APT 1, Roslindale, MA 02131 | condo | $535,000 | 2 | 2 | 1,275 | Yes | Yes |
| 15 S Fairview St #3, Roslindale, MA 02131 | condo | $583,500 | 3 | 1 | 1,475 | Yes | Yes |
| 136A Belgrade Ave, Roslindale, MA 02131 | single-family | $700,000 | 3 | 2 | 1,152 | Yes | Yes |
| 3943 Washington St Floor 2, Roslindale, MA 02131 | condo | $575,000 | 3 | 2 | 1,261 | No | No |
| 737 American Legion Hwy, Roslindale, MA 02131 | single-family | $710,000 | 5 | 3 | 1,755 | Yes | Yes |
| 4370 Washington St #2, Roslindale, MA 02131 | condo | $475,000 | 2 | 1 | 745 | Yes | Yes |
| 11-13 Brookfield St, Roslindale, MA 02131 | multifamily | $929,000 | 5 | 3 | 2,433 | No | No |
| 41 Brown Ave, Roslindale, MA 02131 | single-family | $1,650,000 | 5 | 3 | 3,117 | Yes | Yes |
| 969 Canterbury St, Roslindale, MA 02131 | multifamily | $975,000 | 5 | 2 | 2,044 | Yes | Yes |

## Important finding

The active listing search returned a usable local candidate universe.

However, active listing detail calls have already been shown to be limited by the Zillow detail tool.

Therefore, the Phase 13A candidate table should treat these records as search-level evidence only.

## Local table created

```text
data/interim/active_listing_candidate_table.csv
outputs/tables/active_listing_candidate_summary.csv


---

# Search Pull 7 — Active Listing Candidate Refresh

## Pull date

2026-07-04

## Related phase

Phase 13A / Phase 13B

## Purpose

Refresh active residential listings in Roslindale / ZIP 02131 and use the result as the source context for the active-listing candidate table.

This pull supports the first active candidate-review table.

This is not a valuation model.

This is not a scoring phase.

This is not a buy/sell recommendation.

## Search setup

| Item | Value |
|---|---|
| Search area | Roslindale / ZIP 02131 |
| Property status | Active for-sale listings |
| Listing statuses | active, coming soon, Zillow Preview |
| Property types | single-family, condo, townhome, multifamily |
| Total matching count | 41 |
| Displayed result count | 41 |

## Notable refresh observation

The active listing universe remained at 41 displayed records.

One observed price changed from the prior Phase 13A note:

| Property | Prior observed price | Current observed price |
|---|---:|---:|
| 15 S Fairview St #3, Roslindale, MA 02131 | $583,500 | $579,500 |

This confirms that Zillow search results and listing prices can change over time.

Every Zillow connector pull should preserve a pull date, source context, and local snapshot.

## Fields returned in search response

The active listing search returned these search-level fields:

- address
- city
- state
- ZIP code
- latitude
- longitude
- bad geocode flag
- bedroom count
- bathroom count
- living area square feet
- lot size, when available
- lot size units, when available
- fixture classification
- home type
- listing price
- title, sometimes
- new construction available plan count
- new construction premier builder flag
- open house flag
- VR model flag
- Zillow detail URL

## Additional fields visible in widget state

The Zillow widget state also exposed additional useful fields for many active records:

- `zpid`
- `statusType`
- `statusText`
- `price`
- `priceLabel`
- `countryCurrency`
- `buildingName`, sometimes
- `lotId`, sometimes
- `plid`, sometimes
- `hdpData.homeInfo.homeStatus`
- `hdpData.homeInfo.homeType`
- `hdpData.homeInfo.zestimate`, sometimes
- `hdpData.homeInfo.rentZestimate`, sometimes
- `isUndisclosedAddress`, sometimes

These fields may be useful for future enrichment, but the normalized Phase 13A candidate table should still treat the record as search-level evidence unless detail validation is completed.

## Example active records returned

| Property | Type | Listing price | Beds | Baths | Sqft | Widget Zestimate? | Widget Rent Zestimate? |
|---|---|---:|---:|---:|---:|---:|---:|
| 602 Canterbury St #10U, Roslindale, MA 02131 | townhome | $515,000 | 2 | 2 | 1,251 | No | No |
| 15 S Fairview St #3, Roslindale, MA 02131 | condo | $579,500 | 3 | 1 | 1,475 | Yes | Yes |
| 11 Whipple Ave APT 1, Roslindale, MA 02131 | condo | $535,000 | 2 | 2 | 1,275 | Yes | Yes |
| 26 Neponset Ave, Roslindale, MA 02131 | single-family | $849,000 | 3 | 3 | 1,886 | No | No |
| 737 American Legion Hwy, Roslindale, MA 02131 | single-family | $710,000 | 5 | 3 | 1,755 | Yes | Yes |
| 11-13 Brookfield St, Roslindale, MA 02131 | multifamily | $929,000 | 5 | 3 | 2,433 | No | No |
| 4370 Washington St #2, Roslindale, MA 02131 | condo | $475,000 | 2 | 1 | 745 | Yes | Yes |
| 41 Brown Ave, Roslindale, MA 02131 | single-family | $1,650,000 | 5 | 3 | 3,117 | Yes | Yes |
| 969 Canterbury St, Roslindale, MA 02131 | multifamily | $975,000 | 5 | 2 | 2,044 | Yes | Yes |
| 596 American Legion Hwy APT 3, Roslindale, MA 02131 | condo | $299,000 | 1 | 1 | 624 | Yes | Yes |

## Important finding

The active listing search returned a usable local candidate universe.

However, active listing detail calls have already been shown to be limited by the Zillow detail tool.

Therefore, the Phase 13A candidate table should treat these records as search-level evidence only.

## Local table created

```text
data/interim/active_listing_candidate_table.csv
outputs/tables/active_listing_candidate_summary.csv
