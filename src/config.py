"""
Config loader for the Zillow undervalued-property project.

Purpose:
- Load the config/*.yml files (geography, forbidden language, field
  mapping) that were previously hardcoded/duplicated across scripts and
  src/ modules. See docs/decision_log.md Decision 017.
- Cache each file's parsed contents so repeated calls within one pipeline
  run don't re-read/re-parse the YAML.

This module does not change any values — it centralizes the same constants
that were already in use.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@lru_cache(maxsize=None)
def _load_yaml(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data or {}


def load_geography_config() -> dict[str, Any]:
    """Return config/geography.yml contents."""
    return _load_yaml("geography.yml")


def load_forbidden_language_patterns() -> list[str]:
    """Return the forbidden-language regex pattern strings."""
    return list(load_forbidden_language_config().get("patterns", []))


def load_forbidden_language_config() -> dict[str, Any]:
    """Return config/forbidden_language.yml contents."""
    return _load_yaml("forbidden_language.yml")


def load_home_type_labels() -> dict[str, str]:
    """Return the raw->normalized home_type label mapping."""
    return dict(load_field_mapping_config().get("home_type_labels", {}))


def load_field_mapping_config() -> dict[str, Any]:
    """Return config/field_mapping.yml contents."""
    return _load_yaml("field_mapping.yml")
