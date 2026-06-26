\# Zillow Field Notes



\## Purpose



This document tracks what fields are actually available from the Zillow connector and how reliable those fields appear to be.



The goal is to avoid designing the project around fields that may not exist, may be missing often, or may require manual validation.



This document should be updated after each Zillow connector pull.



\---



\## Current Status



No raw Zillow connector sample has been saved yet.



This document is currently a planning template.



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

