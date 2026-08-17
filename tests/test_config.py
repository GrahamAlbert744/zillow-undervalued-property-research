"""
Tests for src/config.py, the config/*.yml loader (Decision 017).

Covers:
- Each loader returns the expected values from the checked-in config files.
- The forbidden-language list read by scripts/create_property_research_notes.py
  and by scripts/hooks/check_forbidden_language.py is the exact same list,
  which is the whole point of centralizing it — the two checks must not be
  able to drift apart.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (  # noqa: E402
    load_forbidden_language_patterns,
    load_geography_config,
    load_home_type_labels,
)


def test_geography_config_has_expected_keys_and_values() -> None:
    geography = load_geography_config()
    assert geography["target_zip"] == "02131"
    assert geography["target_radius_miles"] == 25.0
    assert isinstance(geography["target_zip_latitude"], float)
    assert isinstance(geography["target_zip_longitude"], float)


def test_forbidden_language_patterns_include_core_phrases() -> None:
    patterns = load_forbidden_language_patterns()
    assert r"\bbuy\b" in patterns
    assert r"\bsell\b" in patterns
    assert "strong buy" in patterns
    assert "safe investment" in patterns


def test_home_type_labels_map_known_variants() -> None:
    labels = load_home_type_labels()
    assert labels["SINGLE_FAMILY"] == "single_family"
    assert labels["CONDO"] == "condo"
    assert labels["MULTI_FAMILY"] == "multi_family"


def _load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_notes_generator_and_hook_use_the_same_forbidden_pattern_list() -> None:
    """
    Regression test for the exact drift risk config extraction was meant to
    close: scripts/create_property_research_notes.py and
    scripts/hooks/check_forbidden_language.py must compile the identical set
    of forbidden-language patterns, because both derive from
    config/forbidden_language.yml.
    """
    scripts_dir = PROJECT_ROOT / "scripts"
    sys.path.insert(0, str(scripts_dir))
    import create_property_research_notes as notes  # noqa: E402

    hook_module = _load_module_from_path(
        "check_forbidden_language",
        PROJECT_ROOT / "scripts" / "hooks" / "check_forbidden_language.py",
    )

    notes_patterns = sorted(pattern.pattern for pattern in notes.FORBIDDEN_PATTERNS)
    hook_patterns = sorted(pattern.pattern for pattern in hook_module.FORBIDDEN_PATTERNS)

    assert notes_patterns == hook_patterns
