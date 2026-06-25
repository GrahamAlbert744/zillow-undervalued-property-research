"""
Field mapping utilities for Zillow connector data.

Goal:
- Load raw Zillow connector output.
- Normalize records into one row per property/listing.
- Create simple derived fields.
- Create basic data-quality flags.

Important:
This module should not score properties yet.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


def safe_get(obj: dict[str, Any], *keys: str) -> Any:
    """Safely get a nested value from a dictionary."""
    current: Any = obj

    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)

    return current


def parse_zpid_from_url(url: str | None) -> str | None:
    """Extract Zillow ZPID from a Zillow URL."""
    if not url:
        return None

    match = re.search(r"/(\d+)_zpid", url)
    if match:
        return match.group(1)

    return None


def normalize_home_type(value: str | None) -> str | None:
    """Normalize home type values."""
    if value is None:
        return None

    value_clean = str(value).strip()

    mapping = {
        "SINGLE_FAMILY": "single_family",
        "singleFamily": "single_family",
        "single_family": "single_family",
        "CONDO": "condo",
        "condo": "condo",
        "TOWNHOUSE": "townhome",
        "townhome": "townhome",
        "MULTI_FAMILY": "multi_family",
        "multiFamily": "multi_family",
        "multi_family": "multi_family",
    }

    return mapping.get(value_clean, value_clean.lower())


def safe_divide(numerator: float | int | None, denominator: float | int | None) -> float | None:
    """Safely divide two numeric values."""
    if numerator is None or denominator is None:
        return None

    try:
        if denominator == 0:
            return None
        return float(numerator) / float(denominator)
    except (TypeError, ValueError):
        return None


def normalize_record(item: dict[str, Any], search_date: str | None = None) -> dict[str, Any]:
    """
    Normalize one Zillow result.

    Supports:
    1. simplified flat sample records
    2. nested Zillow connector search records with {"type": "property", "result": {...}}
    """
    record = item.get("result", item)

    url = record.get("zillow_url") or record.get("homeDetailsPageUrl")
    zpid = record.get("zpid") or parse_zpid_from_url(url)

    formatted_address = record.get("formattedAddress", {})

    line1 = formatted_address.get("line1")
    line2 = formatted_address.get("line2")

    address = record.get("address")
    if address is None and line1 and line2:
        address = f"{line1}, {line2}"
    elif address is None:
        address = line1

    city = record.get("city") or formatted_address.get("city")
    state = record.get("state") or formatted_address.get("stateOrProvince")
    zip_code = record.get("zip_code") or formatted_address.get("postalCode")

    latitude = record.get("latitude")
    if latitude is None:
        latitude = safe_get(record, "geoRegion", "latLong", "latitude")

    longitude = record.get("longitude")
    if longitude is None:
        longitude = safe_get(record, "geoRegion", "latLong", "longitude")

    price = record.get("price")
    if isinstance(price, dict):
        price = price.get("filteredPrice")
    if price is None:
        price = safe_get(record, "price", "filteredPrice")

    beds = record.get("beds")
    if beds is None:
        beds = record.get("bedroomCount")

    baths = record.get("baths")
    if baths is None:
        baths = record.get("bathroomCount")

    square_feet = record.get("square_feet")
    if square_feet is None:
        square_feet = record.get("livingAreaSquareFeet")

    lot_size = record.get("lot_size")
    if lot_size is None:
        lot_size = safe_get(record, "lotArea", "size")

    lot_size_units = record.get("lot_size_units")
    if lot_size_units is None:
        lot_size_units = safe_get(record, "lotArea", "sizeUnits")

    home_type = record.get("home_type") or record.get("homeType")
    home_type = normalize_home_type(home_type)

    new_construction_available_plan_count = safe_get(record, "newConstruction", "availablePlanCnt")
    new_construction_premier_builder = safe_get(record, "newConstruction", "premierBuilder")

    price_per_sqft = safe_divide(price, square_feet)

    zestimate = record.get("zestimate")
    rent_zestimate = record.get("rent_zestimate")

    price_to_zestimate_pct = None
    if zestimate:
        price_to_zestimate_pct = safe_divide(price - zestimate, zestimate)

    annual_rent_zestimate = None
    gross_rent_yield = None
    if rent_zestimate:
        annual_rent_zestimate = rent_zestimate * 12
        gross_rent_yield = safe_divide(annual_rent_zestimate, price)

    normalized = {
        "property_id": zpid,
        "zpid": zpid,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": str(zip_code) if zip_code is not None else None,
        "latitude": latitude,
        "longitude": longitude,
        "is_bad_geocode": safe_get(record, "geoRegion", "isBadGeocode"),
        "home_status": record.get("status_type"),
        "status_text": record.get("status_text"),
        "home_type": home_type,
        "fixture_classification": record.get("fixtureClassification"),
        "price": price,
        "zestimate": zestimate,
        "rent_zestimate": rent_zestimate,
        "beds": beds,
        "baths": baths,
        "square_feet": square_feet,
        "lot_size": lot_size,
        "lot_size_units": lot_size_units,
        "price_per_sqft": price_per_sqft,
        "price_to_zestimate_pct": price_to_zestimate_pct,
        "annual_rent_zestimate": annual_rent_zestimate,
        "gross_rent_yield": gross_rent_yield,
        "new_construction_available_plan_count": new_construction_available_plan_count,
        "new_construction_premier_builder": new_construction_premier_builder,
        "has_open_house": record.get("hasOpenHouse"),
        "has_vr_model": record.get("hasVRModel"),
        "title": record.get("title"),
        "zillow_url": url,
        "search_date": search_date,
        "data_source": "zillow_connector",
    }

    normalized["missing_price"] = normalized["price"] is None
    normalized["missing_square_feet"] = normalized["square_feet"] is None
    normalized["missing_beds"] = normalized["beds"] is None
    normalized["missing_baths"] = normalized["baths"] is None
    normalized["missing_home_type"] = normalized["home_type"] is None
    normalized["missing_lat_long"] = normalized["latitude"] is None or normalized["longitude"] is None
    normalized["missing_zestimate"] = normalized["zestimate"] is None
    normalized["missing_rent_zestimate"] = normalized["rent_zestimate"] is None
    normalized["undisclosed_address"] = bool(address and "undisclosed" in address.lower())

    normalized["invalid_price"] = normalized["price"] is None or normalized["price"] <= 0
    normalized["invalid_square_feet"] = normalized["square_feet"] is None or normalized["square_feet"] <= 0

    normalized["data_needs_review"] = any(
        [
            normalized["missing_price"],
            normalized["missing_square_feet"],
            normalized["missing_beds"],
            normalized["missing_baths"],
            normalized["missing_home_type"],
            normalized["missing_lat_long"],
            normalized["undisclosed_address"],
            normalized["invalid_price"],
            normalized["invalid_square_feet"],
        ]
    )

    return normalized


def load_zillow_raw_json(path: str | Path) -> dict[str, Any]:
    """Load raw Zillow JSON file."""
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_zillow_payload(payload: dict[str, Any]) -> pd.DataFrame:
    """Normalize a Zillow search payload into a dataframe."""
    search_date = payload.get("metadata", {}).get("search_date")
    results = payload.get("results", [])

    rows = [normalize_record(item, search_date=search_date) for item in results]
    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df["possible_duplicate_address"] = (
        df["address"].str.lower().duplicated(keep=False).fillna(False)
    )

    df["possible_duplicate_lat_long"] = (
        df[["latitude", "longitude"]].duplicated(keep=False)
        & df["latitude"].notna()
        & df["longitude"].notna()
    )

    return df


def save_normalized_csv(df: pd.DataFrame, output_path: str | Path) -> None:
    """Save normalized dataframe to CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)