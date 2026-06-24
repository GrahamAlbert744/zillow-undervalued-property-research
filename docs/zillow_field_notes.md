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



\## Search Pull 1



| Item | Value |

|---|---|

| Pull date | TBD |

| Search area | 02131 demo search |

| Search radius | Initial demo; full 25-mile radius later |

| Property types requested | single-family, condo, townhome, multifamily |

| Number of records returned | TBD |

| Raw file path | `data/raw/zillow\_raw\_search\_YYYYMMDD.json` |

| Notes | TBD |



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

