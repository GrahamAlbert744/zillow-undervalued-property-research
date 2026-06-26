"""
Geography utilities for the Zillow undervalued-property project.

Current goal:
- Calculate approximate distance from ZIP 02131 center.
- Flag properties outside the target radius.

This uses the haversine formula and does not require an external API.
"""

from __future__ import annotations

import math
from typing import Optional


# Approximate center point for ZIP 02131 / Roslindale.
# This can be refined later if needed.
ZIP_02131_LATITUDE = 42.2834
ZIP_02131_LONGITUDE = -71.1290
EARTH_RADIUS_MILES = 3958.8


def haversine_distance_miles(
    lat1: float | None,
    lon1: float | None,
    lat2: float | None = ZIP_02131_LATITUDE,
    lon2: float | None = ZIP_02131_LONGITUDE,
) -> Optional[float]:
    """
    Calculate distance in miles between two latitude/longitude points.

    Returns None if any coordinate is missing.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None

    try:
        lat1_rad = math.radians(float(lat1))
        lon1_rad = math.radians(float(lon1))
        lat2_rad = math.radians(float(lat2))
        lon2_rad = math.radians(float(lon2))
    except (TypeError, ValueError):
        return None

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_MILES * c


def is_outside_radius(
    distance_miles: float | None,
    radius_miles: float = 25.0,
) -> bool:
    """
    Return True if a property is outside the target radius.

    Missing distance is not treated as outside; it should be handled
    separately with a missing_lat_long / needs_review flag.
    """
    if distance_miles is None:
        return False

    return distance_miles > radius_miles