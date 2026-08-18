"""
Create per-property research notes.

Purpose:
- Turn each non-excluded research-queue row into a human-readable note.
- Use only available evidence; explicitly list missing information.
- Do NOT make a purchase or sale recommendation.
- Do NOT claim a property is undervalued without validation.
- Do NOT create a completed valuation.

Input:
- data/interim/property_research_queue.csv

Output:
- outputs/property_research_notes/*.md (one file per property)
- outputs/tables/property_research_notes_summary.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

try:
    from src.config import load_forbidden_language_patterns
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config import load_forbidden_language_patterns


INPUT_PATH = Path("data/interim/property_research_queue.csv")
NOTES_DIR = Path("outputs/property_research_notes")
SUMMARY_PATH = Path("outputs/tables/property_research_notes_summary.csv")

# Buckets already fully explained in candidate_exclusion_review_table.csv.
SKIP_QUEUE_BUCKETS = {"excluded"}

# Sourced from config/forbidden_language.yml (Decision 017). Also read by
# scripts/hooks/check_forbidden_language.py so both the generation-time
# check and the edit-time hook stay in sync.
FORBIDDEN_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in load_forbidden_language_patterns()
]


def fmt(value: object, none_text: str = "not available") -> str:
    """Format a scalar value for markdown, handling missing values."""
    if value is None or (isinstance(value, float) and pd.isna(value)) or pd.isna(value):
        return none_text
    return str(value)


def fmt_bool(value: object) -> str:
    """Format a boolean-ish value as yes/no/unknown."""
    if pd.isna(value):
        return "unknown"
    return "yes" if bool(value) else "no"


def fmt_money(value: object) -> str:
    """Format a numeric value as a dollar amount."""
    if value is None or pd.isna(value):
        return "not available"
    return f"${float(value):,.0f}"


def fmt_pct(value: object) -> str:
    """Format a numeric value as a percentage."""
    if value is None or pd.isna(value):
        return "not available"
    return f"{float(value):.1f}%"


def build_property_summary(row: pd.Series) -> list[str]:
    """Section: property_summary."""
    return [
        "## Property Summary",
        "",
        f"- Address: {fmt(row['address'])}",
        f"- Home type: {fmt(row['home_type'])}",
        f"- Status: {fmt(row['status_text'])} (`{fmt(row['home_status'])}`)",
        f"- Listing price: {fmt_money(row['price'])}",
        f"- Beds / Baths: {fmt(row['beds'])} / {fmt(row['baths'])}",
        f"- Square feet: {fmt(row['square_feet'])}",
        f"- Lot size: {fmt(row['lot_size'])} {fmt(row['lot_size_units'], '')}".strip(),
        f"- Price per sqft: {fmt(row['price_per_sqft'])}",
        f"- Distance from ZIP 02131: {fmt(row['distance_from_02131_miles'])} miles",
        f"- Zillow URL: {fmt(row['zillow_url'])}",
        f"- Pull date / source: {fmt(row['search_date'])} / {fmt(row['data_source'])}",
        f"- Research label: **{fmt(row['conservative_output_label'])}** "
        f"(queue position: {fmt(row['research_queue_position'])}, "
        f"internal bucket: `{fmt(row['research_queue_bucket'])}`, "
        f"priority: `{fmt(row['research_priority'])}`)",
        "",
    ]


def build_available_evidence(row: pd.Series) -> list[str]:
    """Section: available_zillow_evidence."""
    lines = [
        "## Available Zillow Evidence",
        "",
        "This is a search-level connector record. It has not gone through a "
        "detail-level pull." if bool(row["search_level_record_only"]) else
        "This record has evidence beyond the basic search-level fields.",
        "",
        f"- Price: {fmt_money(row['price'])}",
        f"- Beds / Baths / Square feet: {fmt(row['beds'])} / {fmt(row['baths'])} / {fmt(row['square_feet'])}",
        f"- Zestimate: {fmt_money(row['zestimate']) if bool(row['zestimate_available']) else 'not available'}",
        f"- Rent Zestimate: {fmt_money(row['rent_zestimate']) if bool(row['rent_zestimate_available']) else 'not available'}",
        f"- Detail-level pull completed: {fmt_bool(row['detail_pull_completed'])}",
        "",
    ]
    return lines


def build_valuation_context_signals(row: pd.Series) -> list[str]:
    """Section: valuation_context_signals."""
    lines = [
        "## Valuation Context Signals",
        "",
        (
            "These are context signals, not a valuation score and not proof "
            "of undervaluation."
        ),
        "",
        f"- Price per sqft vs. home-type median: {fmt_pct(row['price_per_sqft_vs_home_type_median_pct'])}",
        f"- Below home-type median price per sqft: {fmt_bool(row['below_home_type_median_ppsf'])}",
        f"- Far below home-type median price per sqft: {fmt_bool(row['far_below_home_type_median_ppsf'])}",
        f"- Zestimate available: {fmt_bool(row['zestimate_available'])}",
    ]

    if bool(row["zestimate_available"]):
        lines.append(f"- Price to Zestimate ratio: {fmt_pct(row['price_to_zestimate_pct'])}")
        lines.append(
            f"- Listing price below Zestimate context: {fmt_bool(row['listing_price_below_zestimate_context'])}"
        )
    else:
        lines.append("- Price-to-Zestimate context not available (no Zestimate returned).")

    lines.extend(
        [
            f"- Valuation context signal count: {fmt(row['valuation_context_signal_count'])}",
            f"- Valuation context bucket: `{fmt(row['valuation_context_bucket'])}`",
            f"- Context confidence notes: {fmt(row['context_confidence_notes'])}",
            "",
        ]
    )
    return lines


def build_income_context_signals(row: pd.Series) -> list[str]:
    """Section: income_context_signals."""
    if not bool(row["rent_zestimate_available"]):
        return [
            "## Income Context Signals",
            "",
            "Rent Zestimate not available. No income context signal for this property.",
            "",
        ]

    return [
        "## Income Context Signals",
        "",
        (
            "Rent Zestimate is an estimate, not a confirmed market rent, and "
            "does not include expense, vacancy, or lease-term assumptions."
        ),
        "",
        f"- Annual Rent Zestimate: {fmt_money(row['annual_rent_zestimate'])}",
        f"- Gross rent yield: {fmt_pct(row['gross_rent_yield'])}",
        f"- Moderate gross rent yield context: {fmt_bool(row['moderate_gross_rent_yield_context'])}",
        f"- High gross rent yield context: {fmt_bool(row['high_gross_rent_yield_context'])}",
        "",
    ]


def build_data_quality_warnings(row: pd.Series) -> list[str]:
    """Section: data_quality_warnings."""
    return [
        "## Data Quality Warnings",
        "",
        f"- Candidate state: `{fmt(row['candidate_state'])}` (review bucket: `{fmt(row['candidate_review_bucket'])}`)",
        f"- Flagged for data-quality review: {fmt_bool(row['data_needs_review'])}",
        f"- Outside target radius: {fmt_bool(row['outside_target_radius'])}",
        f"- Search-level record only: {fmt_bool(row['search_level_record_only'])}",
        f"- Detail pull completed: {fmt_bool(row['detail_pull_completed'])}",
        "",
    ]


def build_missing_information(row: pd.Series) -> list[str]:
    """Section: missing_information."""
    missing: list[str] = []

    if not bool(row["zestimate_available"]):
        missing.append("Zestimate")

    if not bool(row["rent_zestimate_available"]):
        missing.append("Rent Zestimate")

    if pd.isna(row["distance_from_02131_miles"]):
        missing.append("Latitude/longitude and distance validation")

    if not bool(row["detail_pull_completed"]):
        missing.extend(
            [
                "Days on market",
                "Price history",
                "Tax history",
                "HOA fee",
                "Listing description",
            ]
        )

    lines = ["## Missing Information", ""]

    if missing:
        lines.extend(f"- {item}" for item in missing)
    else:
        lines.append("- No known missing fields at this time.")

    lines.append("")
    return lines


def build_next_research_steps(row: pd.Series) -> list[str]:
    """Section: next_human_research_steps."""
    steps_text = fmt(row["next_research_steps"], "")
    steps = [step.strip() for step in steps_text.split(".") if step.strip()]

    lines = ["## Next Human Research Steps", ""]

    if steps:
        lines.extend(f"- {step}." for step in steps)
    else:
        lines.append("- Manually confirm listing details.")

    lines.append("")
    return lines


def build_interpretation_cautions(row: pd.Series) -> list[str]:
    """Section: interpretation_cautions."""
    return [
        "## Interpretation Cautions",
        "",
        (
            "Appearance in the research queue reflects workflow ordering and "
            "available context signals. It does not mean this property is "
            "undervalued, confirmed, or investment-ready."
        ),
        (
            "This note does not recommend buying or selling this property. "
            "It may deserve human review, has a context signal that needs "
            "validation, and requires manual confirmation before any "
            "financial decision."
        ),
        (
            "Zestimate is context, not an appraisal. Rent Zestimate is "
            "context, not a confirmed market rent."
        ),
        "",
        f"- Research queue is not an investment ranking: {fmt_bool(row['research_queue_not_investment_ranking'])}",
        f"- Final score created: {fmt_bool(row['final_score_created'])}",
        f"- Investment recommendation created: {fmt_bool(row['investment_recommendation_created'])}",
        f"- Purchase/sale recommendation created: {fmt_bool(row['buy_sell_recommendation_created'])}",
        f"- Backtesting ready: {fmt_bool(row['backtesting_ready'])}",
        "",
    ]


def check_forbidden_language(text: str) -> list[str]:
    """Return any forbidden phrases found in the note text."""
    matches = []
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            matches.append(pattern.pattern)
    return matches


def build_note(row: pd.Series) -> str:
    """Assemble the full markdown note for one property."""
    lines = [
        f"# Property Research Note: {fmt(row['address'])}",
        "",
        (
            "This note is generated for human research triage only. It is "
            "not a purchase or sale recommendation and does not represent "
            "a completed valuation."
        ),
        "",
    ]

    lines.extend(build_property_summary(row))
    lines.extend(build_available_evidence(row))
    lines.extend(build_valuation_context_signals(row))
    lines.extend(build_income_context_signals(row))
    lines.extend(build_data_quality_warnings(row))
    lines.extend(build_missing_information(row))
    lines.extend(build_next_research_steps(row))
    lines.extend(build_interpretation_cautions(row))

    return "\n".join(lines)


def note_file_name(row: pd.Series) -> str:
    """Build a stable, sortable file name for the note."""
    position = int(row["research_queue_position"]) if pd.notna(row["research_queue_position"]) else 0
    return f"{position:03d}_property_{row['property_id']}.md"


def create_notes() -> pd.DataFrame:
    """Generate research notes for every non-excluded queue row."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}. "
            "Run scripts/create_research_queue_table.py first."
        )

    queue_df = pd.read_csv(INPUT_PATH)
    queue_df = queue_df[~queue_df["research_queue_bucket"].isin(SKIP_QUEUE_BUCKETS)].copy()

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []

    for _, row in queue_df.iterrows():
        note_text = build_note(row)
        forbidden_matches = check_forbidden_language(note_text)

        if forbidden_matches:
            raise ValueError(
                f"Forbidden language {forbidden_matches} found in note for "
                f"property_id={row['property_id']}. Aborting before writing output."
            )

        file_name = note_file_name(row)
        note_path = NOTES_DIR / file_name
        note_path.write_text(note_text, encoding="utf-8")

        summary_rows.append(
            {
                "property_id": row["property_id"],
                "address": row["address"],
                "research_queue_position": row["research_queue_position"],
                "research_queue_bucket": row["research_queue_bucket"],
                "research_priority": row["research_priority"],
                "note_path": str(note_path),
                "forbidden_language_detected": bool(forbidden_matches),
            }
        )

    return pd.DataFrame(summary_rows)


def main() -> None:
    """Create property research notes and their summary table."""
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary_df = create_notes()
    summary_df.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved {len(summary_df)} property research notes to: {NOTES_DIR}")
    print(f"Saved property research notes summary to: {SUMMARY_PATH}")
    print()
    print("Important:")
    print("- These notes are for human research triage only.")
    print("- No purchase or sale recommendations were created.")
    print("- No property is claimed to be undervalued without validation.")


if __name__ == "__main__":
    main()
