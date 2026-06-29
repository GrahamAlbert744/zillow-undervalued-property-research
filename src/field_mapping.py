"""
Field mapping utilities for the Zillow undervalued-property project.

Purpose:
- Load raw Zillow JSON.
- Normalize raw Zillow connector records into one row per property/listing.
- Support both:
    1. flat local development samples
    2. nested Zillow connector search results
- Add basic derived fields:
    - price_per_sqft
    - price_to_zestimate_pct
    - annual_rent_zestimate
    - gross_rent_yield
    - distance_from_02131_miles
    - outside_target_radius

This file does not score properties.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Optional

import pandas as pd

try:
    from src.geocoding import haversine_distance_miles, is_outside_radius
except ModuleNotFoundError:
    from geocoding import haversine_distance_miles, is_outside_radius


DEFAULT_RAW_PATH = Path("data/raw/zillow_raw_search_20260624.json")
DEFAULT_OUTPUT_PATH = Path("data/processed/all_properties_normalized.csv")


def get_nested(data: dict[str, Any], path: list[str], default: Any = None) -> Any:
    """Safely retrieve a nested dictionary value."""
    current: Any = data

    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

        if current is None:
            return default

    return current


def clean_text(value: Any) -> Optional[str]:
    """Return stripped text or None."""
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    return text


def to_float(value: Any) -> Optional[float]:
    """Convert a value to float when possible."""
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int_or_float(value: Any) -> Optional[float]:
    """Convert numeric-like values while preserving missing values."""
    return to_float(value)


def extract_zpid(record: dict[str, Any]) -> Optional[str]:
    """Extract ZPID from explicit field or Zillow URL."""
    zpid = record.get("zpid") or record.get("property_id")

    if zpid is not None:
        return str(zpid)

    url = (
        record.get("zillow_url")
        or record.get("homeDetailsPageUrl")
        or get_nested(record, ["hdpData", "homeInfo", "homeDetailsPageUrl"])
    )

    if not url:
        return None

    match = re.search(r"/(\d+)_zpid", str(url))

    if match:
        return match.group(1)

    return None


def normalize_home_type(value: Any) -> Optional[str]:
    """Normalize Zillow home type labels."""
    if value is None:
        return None

    raw = str(value).strip()

    mapping = {
        "SINGLE_FAMILY": "single_family",
        "singleFamily": "single_family",
        "single_family": "single_family",
        "house": "single_family",
        "CONDO": "condo",
        "condo": "condo",
        "TOWNHOUSE": "townhome",
        "townhouse": "townhome",
        "townhome": "townhome",
        "MULTI_FAMILY": "multi_family",
        "multiFamily": "multi_family",
        "multi_family": "multi_family",
        "multifamily": "multi_family",
    }

    return mapping.get(raw, raw.lower())


def build_address(record: dict[str, Any]) -> Optional[str]:
    """Build address from flat or nested Zillow fields."""
    flat_address = clean_text(record.get("address"))

    if flat_address:
        return flat_address

    line1 = clean_text(get_nested(record, ["formattedAddress", "line1"]))
    line2 = clean_text(get_nested(record, ["formattedAddress", "line2"]))

    if line1 and line2:
        return f"{line1}, {line2}"

    if line1:
        city = clean_text(get_nested(record, ["formattedAddress", "city"]))
        state = clean_text(get_nested(record, ["formattedAddress", "stateOrProvince"]))
        zip_code = clean_text(get_nested(record, ["formattedAddress", "postalCode"]))

        parts = [line1]

        city_state_zip = " ".join(part for part in [state, zip_code] if part)

        if city and city_state_zip:
            parts.append(f"{city}, {city_state_zip}")
        elif city:
            parts.append(city)
        elif city_state_zip:
            parts.append(city_state_zip)

        return ", ".join(parts)

    return None


def extract_price(record: dict[str, Any]) -> Optional[float]:
    """Extract listing price from flat or nested fields."""
    candidates = [
        record.get("price"),
        get_nested(record, ["price", "filteredPrice"]),
        get_nested(record, ["price", "value"]),
        get_nested(record, ["hdpData", "homeInfo", "price"]),
    ]

    for candidate in candidates:
        numeric_value = to_float(candidate)
        if numeric_value is not None:
            return numeric_value

    return None


def extract_records(payload: Any) -> list[dict[str, Any]]:
    """
    Extract property records from supported raw payload shapes.

    Supported shapes:
    - {"results": [...]}
    - [...]
    - {"result": {...}}
    """
    if isinstance(payload, list):
        raw_records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("results"), list):
        raw_records = payload["results"]
    elif isinstance(payload, dict) and isinstance(payload.get("result"), dict):
        raw_records = [payload]
    else:
        raw_records = []

    records: list[dict[str, Any]] = []

    for item in raw_records:
        if not isinstance(item, dict):
            continue

        # Zillow connector search results often look like:
        # {"type": "property", "result": {...}}
        if isinstance(item.get("result"), dict):
            records.append(item["result"])
        else:
            records.append(item)

    return records


def normalize_single_record(
    record: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize one Zillow property/listing record."""
    metadata = metadata or {}

    zpid = extract_zpid(record)
    property_id = zpid

    address = build_address(record)

    city = clean_text(
        record.get("city")
        or get_nested(record, ["formattedAddress", "city"])
    )

    state = clean_text(
        record.get("state")
        or get_nested(record, ["formattedAddress", "stateOrProvince"])
    )

    zip_code = clean_text(
        record.get("zip_code")
        or record.get("postalCode")
        or get_nested(record, ["formattedAddress", "postalCode"])
    )

    latitude = to_float(
        record.get("latitude")
        or get_nested(record, ["geoRegion", "latLong", "latitude"])
    )

    longitude = to_float(
        record.get("longitude")
        or get_nested(record, ["geoRegion", "latLong", "longitude"])
    )

    is_bad_geocode = get_nested(record, ["geoRegion", "isBadGeocode"])

    home_status = clean_text(
        record.get("home_status")
        or record.get("status_type")
        or record.get("homeStatus")
        or get_nested(record, ["hdpData", "homeInfo", "homeStatus"])
    )

    status_text = clean_text(
        record.get("status_text")
        or record.get("statusText")
        or get_nested(record, ["hdpData", "homeInfo", "statusText"])
    )

    home_type = normalize_home_type(
        record.get("home_type")
        or record.get("homeType")
        or get_nested(record, ["hdpData", "homeInfo", "homeType"])
    )

    fixture_classification = clean_text(record.get("fixtureClassification"))

    price = extract_price(record)

    zestimate = to_float(
        record.get("zestimate")
        or record.get("zestimateAmount")
        or get_nested(record, ["hdpData", "homeInfo", "zestimate"])
    )

    rent_zestimate = to_float(
        record.get("rent_zestimate")
        or record.get("rentZestimate")
        or get_nested(record, ["hdpData", "homeInfo", "rentZestimate"])
    )

    beds = to_int_or_float(
        record.get("beds")
        or record.get("bedroomCount")
        or get_nested(record, ["hdpData", "homeInfo", "bedrooms"])
    )

    baths = to_int_or_float(
        record.get("baths")
        or record.get("bathroomCount")
        or get_nested(record, ["hdpData", "homeInfo", "bathrooms"])
    )

    square_feet = to_float(
        record.get("square_feet")
        or record.get("livingAreaSquareFeet")
        or get_nested(record, ["hdpData", "homeInfo", "livingArea"])
    )

    lot_size = to_float(
        record.get("lot_size")
        or get_nested(record, ["lotArea", "size"])
        or get_nested(record, ["hdpData", "homeInfo", "lotAreaValue"])
    )

    lot_size_units = clean_text(
        record.get("lot_size_units")
        or get_nested(record, ["lotArea", "sizeUnits"])
        or get_nested(record, ["hdpData", "homeInfo", "lotAreaUnit"])
    )

    new_construction_available_plan_count = to_float(
        get_nested(record, ["newConstruction", "availablePlanCnt"], default=0)
    )

    new_construction_premier_builder = get_nested(
        record,
        ["newConstruction", "premierBuilder"],
        default=False,
    )

    has_open_house = record.get("hasOpenHouse")
    has_vr_model = record.get("hasVRModel")

    title = clean_text(record.get("title"))

    zillow_url = clean_text(
        record.get("zillow_url")
        or record.get("homeDetailsPageUrl")
        or get_nested(record, ["hdpData", "homeInfo", "homeDetailsPageUrl"])
    )

    search_date = clean_text(metadata.get("search_date")) or str(date.today())
    data_source = clean_text(metadata.get("source")) or "zillow_connector"

    if price is not None and square_feet not in (None, 0):
        price_per_sqft = price / square_feet
    else:
        price_per_sqft = None

    if price is not None and zestimate not in (None, 0):
        price_to_zestimate_pct = (price - zestimate) / zestimate
    else:
        price_to_zestimate_pct = None

    if rent_zestimate is not None:
        annual_rent_zestimate = rent_zestimate * 12
    else:
        annual_rent_zestimate = None

    if annual_rent_zestimate is not None and price not in (None, 0):
        gross_rent_yield = annual_rent_zestimate / price
    else:
        gross_rent_yield = None

    distance_from_02131_miles = haversine_distance_miles(latitude, longitude)
    outside_target_radius = is_outside_radius(distance_from_02131_miles)

    normalized = {
        "property_id": property_id,
        "zpid": zpid,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude,
        "is_bad_geocode": is_bad_geocode,
        "distance_from_02131_miles": (
            round(distance_from_02131_miles, 2)
            if distance_from_02131_miles is not None
            else None
        ),
        "outside_target_radius": outside_target_radius,
        "home_status": home_status,
        "status_text": status_text,
        "home_type": home_type,
        "fixture_classification": fixture_classification,
        "price": price,
        "zestimate": zestimate,
        "rent_zestimate": rent_zestimate,
        "beds": beds,
        "baths": baths,
        "square_feet": square_feet,
        "lot_size": lot_size,
        "lot_size_units": lot_size_units,
        "price_per_sqft": (
            round(price_per_sqft, 2)
            if price_per_sqft is not None
            else None
        ),
        "price_to_zestimate_pct": (
            round(price_to_zestimate_pct, 4)
            if price_to_zestimate_pct is not None
            else None
        ),
        "annual_rent_zestimate": annual_rent_zestimate,
        "gross_rent_yield": (
            round(gross_rent_yield, 4)
            if gross_rent_yield is not None
            else None
        ),
        "new_construction_available_plan_count": new_construction_available_plan_count,
        "new_construction_premier_builder": new_construction_premier_builder,
        "has_open_house": has_open_house,
        "has_vr_model": has_vr_model,
        "title": title,
        "zillow_url": zillow_url,
        "search_date": search_date,
        "data_source": data_source,
    }

    return normalized


def load_zillow_raw_json(path: str | Path = DEFAULT_RAW_PATH) -> dict[str, Any]:
    """Load raw Zillow JSON from disk."""
    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_zillow_payload(payload: dict[str, Any] | list[Any]) -> pd.DataFrame:
    """Normalize a raw Zillow payload into a dataframe."""
    metadata = payload.get("metadata", {}) if isinstance(payload, dict) else {}
    records = extract_records(payload)

    normalized_records = [
        normalize_single_record(record, metadata=metadata)
        for record in records
    ]

    df = pd.DataFrame(normalized_records)

    preferred_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "latitude",
        "longitude",
        "is_bad_geocode",
        "distance_from_02131_miles",
        "outside_target_radius",
        "home_status",
        "status_text",
        "home_type",
        "fixture_classification",
        "price",
        "zestimate",
        "rent_zestimate",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "price_to_zestimate_pct",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "new_construction_available_plan_count",
        "new_construction_premier_builder",
        "has_open_house",
        "has_vr_model",
        "title",
        "zillow_url",
        "search_date",
        "data_source",
    ]

    for column in preferred_columns:
        if column not in df.columns:
            df[column] = None

    return df[preferred_columns]


def save_normalized_csv(
    df: pd.DataFrame,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """Save normalized dataframe to CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    """Run field mapping directly for a quick manual test."""
    payload = load_zillow_raw_json(DEFAULT_RAW_PATH)
    df = normalize_zillow_payload(payload)
    save_normalized_csv(df, DEFAULT_OUTPUT_PATH)

    print(f"Loaded raw records: {len(extract_records(payload))}")
    print(f"Normalized rows: {len(df)}")
    print(f"Saved normalized CSV to: {DEFAULT_OUTPUT_PATH}")
    print()
    print(
        df[
            [
                "address",
                "city",
                "home_type",
                "price",
                "square_feet",
                "price_per_sqft",
                "distance_from_02131_miles",
                "outside_target_radius",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()