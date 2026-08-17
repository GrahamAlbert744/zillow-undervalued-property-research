"""
Create the MVP run summary report.

Purpose:
- Roll up counts across the full MVP pipeline (normalize -> gates ->
  candidate table -> valuation context -> research scoring -> research
  queue -> exclusion review -> research notes).
- Confirm anti-overclaim safeguards are still in place.
- Surface remaining limitations. Do not recommend buying or selling.

Inputs (all optional except the normalized table; missing tables are
reported as not available rather than causing a crash):
- data/processed/all_properties_normalized.csv
- outputs/tables/active_listing_candidate_summary.csv
- outputs/tables/valuation_context_feature_summary.csv
- outputs/tables/undervaluation_scores_summary.csv
- outputs/tables/property_research_queue_summary.csv
- outputs/tables/candidate_exclusion_review_summary.csv
- outputs/tables/property_research_notes_summary.csv

Output:
- outputs/reports/mvp_run_summary.md
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


NORMALIZED_PATH = Path("data/processed/all_properties_normalized.csv")
CANDIDATE_SUMMARY_PATH = Path("outputs/tables/active_listing_candidate_summary.csv")
VALUATION_SUMMARY_PATH = Path("outputs/tables/valuation_context_feature_summary.csv")
SCORES_SUMMARY_PATH = Path("outputs/tables/undervaluation_scores_summary.csv")
QUEUE_SUMMARY_PATH = Path("outputs/tables/property_research_queue_summary.csv")
EXCLUSION_SUMMARY_PATH = Path("outputs/tables/candidate_exclusion_review_summary.csv")
NOTES_SUMMARY_PATH = Path("outputs/tables/property_research_notes_summary.csv")
REPORT_PATH = Path("outputs/reports/mvp_run_summary.md")


def read_metric_table(path: Path) -> dict[str, str] | None:
    """Read a metric/value summary CSV into a dict. Return None if missing."""
    if not path.exists():
        return None

    df = pd.read_csv(path)

    if "metric" not in df.columns or "value" not in df.columns:
        return None

    return dict(zip(df["metric"].astype(str), df["value"].astype(str)))


def metric_line(metrics: dict[str, str] | None, key: str, label: str) -> str:
    """Build one markdown bullet for a metric, tolerating a missing table."""
    if metrics is None:
        return f"- {label}: table not available"

    value = metrics.get(key, "not available")
    return f"- {label}: **{value}**"


def build_input_files_section() -> list[str]:
    """List every input this report attempted to read."""
    paths = [
        NORMALIZED_PATH,
        CANDIDATE_SUMMARY_PATH,
        VALUATION_SUMMARY_PATH,
        SCORES_SUMMARY_PATH,
        QUEUE_SUMMARY_PATH,
        EXCLUSION_SUMMARY_PATH,
        NOTES_SUMMARY_PATH,
    ]

    lines = ["## Input files", ""]
    for path in paths:
        status = "found" if path.exists() else "not found"
        lines.append(f"- `{path}` ({status})")
    lines.append("")
    return lines


def build_data_quality_section(
    total_records: int, candidate_metrics: dict[str, str] | None
) -> list[str]:
    """Section answering the doc's data_quality review questions."""
    lines = [
        "## Data Quality",
        "",
        f"- Total normalized active-listing records pulled: **{total_records}**",
        metric_line(candidate_metrics, "rankable_later_count", "Rankable-later candidates"),
        metric_line(candidate_metrics, "needs_review_count", "Needs-review candidates"),
        metric_line(candidate_metrics, "hold_count", "Held candidates"),
        metric_line(candidate_metrics, "reject_count", "Rejected candidates"),
        metric_line(candidate_metrics, "missing_lat_long_count", "Missing latitude/longitude"),
        metric_line(candidate_metrics, "undisclosed_address_count", "Undisclosed addresses"),
        "",
    ]
    return lines


def build_valuation_context_section(valuation_metrics: dict[str, str] | None) -> list[str]:
    """Section answering the doc's valuation_context review questions."""
    return [
        "## Valuation Context",
        "",
        metric_line(
            valuation_metrics, "basic_price_context_available",
            "Properties with price-per-sqft context",
        ),
        metric_line(
            valuation_metrics, "zestimate_context_available",
            "Properties with Zestimate context",
        ),
        metric_line(
            valuation_metrics, "income_context_available",
            "Properties with Rent Zestimate / income context",
        ),
        metric_line(
            valuation_metrics, "far_below_home_type_median_ppsf",
            "Properties far below home-type median price per sqft",
        ),
        "",
        "Reminder: these are context signals, not a valuation score.",
        metric_line(valuation_metrics, "valuation_score_created", "Valuation score created"),
        "",
    ]


def build_research_scoring_section(scores_metrics: dict[str, str] | None) -> list[str]:
    """Section covering the Decision 019 research-ranking score."""
    return [
        "## Research Scoring",
        "",
        metric_line(scores_metrics, "scored_records", "Properties scored"),
        metric_line(
            scores_metrics, "not_scored_excluded_by_candidate_gating",
            "Properties not scored (excluded by candidate gating)",
        ),
        metric_line(
            scores_metrics, "max_achievable_research_score",
            "Max achievable research score (of 100; remaining points reserved "
            "for signals not yet implemented)",
        ),
        metric_line(scores_metrics, "median_total_research_score", "Median research score"),
        "",
        "This is a transparent research-ranking score for human triage only "
        "(docs/scoring_methodology.md). It is not a final/validated score, "
        "not an investment ranking, and not a purchase or sale recommendation.",
        "",
    ]


def build_research_queue_section(queue_metrics: dict[str, str] | None) -> list[str]:
    """Section answering the doc's research_queue review questions."""
    return [
        "## Research Queue",
        "",
        metric_line(queue_metrics, "review_first_count", "review_first"),
        metric_line(queue_metrics, "review_next_count", "review_next"),
        metric_line(queue_metrics, "review_if_time_count", "review_if_time"),
        metric_line(queue_metrics, "watchlist_limited_data_count", "watchlist_limited_data"),
        metric_line(queue_metrics, "data_quality_review_count", "data_quality_review"),
        metric_line(queue_metrics, "excluded_count", "excluded"),
        "",
    ]


def build_exclusion_review_section(exclusion_metrics: dict[str, str] | None) -> list[str]:
    """Section covering the candidate exclusion/hold review table."""
    return [
        "## Exclusion / Hold Review",
        "",
        metric_line(
            exclusion_metrics, "records_in_exclusion_review_table",
            "Properties preserved in the exclusion/hold review table",
        ),
        metric_line(exclusion_metrics, "reject_count", "Reject"),
        metric_line(exclusion_metrics, "hold_count", "Hold"),
        metric_line(exclusion_metrics, "needs_review_count", "Needs review"),
        "",
        "No excluded or held property was silently dropped from the pipeline.",
        "",
    ]


def build_research_notes_section(notes_summary_path: Path) -> list[str]:
    """Section covering the property research notes output."""
    if not notes_summary_path.exists():
        return [
            "## Property Research Notes",
            "",
            "Notes summary table not available. Run "
            "scripts/create_property_research_notes.py.",
            "",
        ]

    notes_df = pd.read_csv(notes_summary_path)
    forbidden_count = (
        int(notes_df["forbidden_language_detected"].sum())
        if "forbidden_language_detected" in notes_df.columns
        else "not tracked"
    )

    return [
        "## Property Research Notes",
        "",
        f"- Notes generated: **{len(notes_df)}**",
        f"- Notes with forbidden buy/sell language detected: **{forbidden_count}**",
        "",
    ]


def build_anti_overclaim_section(queue_metrics: dict[str, str] | None) -> list[str]:
    """Confirm the safeguards this pipeline promises."""
    return [
        "## Anti-Overclaim Safeguards",
        "",
        metric_line(queue_metrics, "final_score_created_count", "Final scores created"),
        metric_line(
            queue_metrics, "investment_recommendation_created_count",
            "Investment recommendations created",
        ),
        metric_line(
            queue_metrics, "buy_sell_recommendation_created_count",
            "Buy/sell recommendations created",
        ),
        metric_line(queue_metrics, "backtesting_ready_count", "Records backtesting-ready"),
        "",
        "All four counts above should read 0 for this pipeline to remain MVP-safe.",
        "",
    ]


def build_limitations_section() -> list[str]:
    """Section answering the doc's limitations review questions."""
    return [
        "## Limitations",
        "",
        "- Active-listing detail pulls are not depended on for this pipeline; "
        "days on market, price history, tax history, HOA fee, and listing "
        "description remain unavailable for every record.",
        "- Recently sold search prices are not confirmed final sale prices "
        "and are not used for backtesting.",
        "- Zestimate and Rent Zestimate are context signals, not an appraisal "
        "or confirmed market rent.",
        "- The research-ranking score (Decision 019) only implements the "
        "signals available from the current search-level data; roughly "
        "18 of 100 points are reserved for signals not yet built (comparable-"
        "sale discount, price-cut/days-on-market history, HOA/tax burden, "
        "multifamily rental-use potential) and always score 0 for now.",
        "- No investment recommendation or buy/sell recommendation has been "
        "built. This report only summarizes the conservative research "
        "pipeline described in the project instructions.",
        "",
    ]


def main() -> None:
    """Create the MVP run summary report."""
    if not NORMALIZED_PATH.exists():
        raise FileNotFoundError(
            f"Normalized file not found: {NORMALIZED_PATH}. "
            "Run scripts/build_property_database.py first."
        )

    normalized_df = pd.read_csv(NORMALIZED_PATH)
    total_records = len(normalized_df)

    candidate_metrics = read_metric_table(CANDIDATE_SUMMARY_PATH)
    valuation_metrics = read_metric_table(VALUATION_SUMMARY_PATH)
    scores_metrics = read_metric_table(SCORES_SUMMARY_PATH)
    queue_metrics = read_metric_table(QUEUE_SUMMARY_PATH)
    exclusion_metrics = read_metric_table(EXCLUSION_SUMMARY_PATH)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "# Zillow MVP Pipeline Run Summary",
        "",
        f"Run created: `{run_time}`",
        "",
        "## Purpose",
        "",
        (
            "Roll up the full conservative MVP pipeline: normalization, "
            "data-quality gates, candidate gating, valuation/context "
            "features, research scoring, research queue, exclusion/hold "
            "review, and property research notes. This report is for "
            "workflow tracking only. It does not recommend buying or "
            "selling any property."
        ),
        "",
    ]

    report_lines.extend(build_input_files_section())
    report_lines.extend(build_data_quality_section(total_records, candidate_metrics))
    report_lines.extend(build_valuation_context_section(valuation_metrics))
    report_lines.extend(build_research_scoring_section(scores_metrics))
    report_lines.extend(build_research_queue_section(queue_metrics))
    report_lines.extend(build_exclusion_review_section(exclusion_metrics))
    report_lines.extend(build_research_notes_section(NOTES_SUMMARY_PATH))
    report_lines.extend(build_anti_overclaim_section(queue_metrics))
    report_lines.extend(build_limitations_section())

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    print(f"Saved MVP run summary to: {REPORT_PATH}")
    print(f"Total normalized records: {total_records}")


if __name__ == "__main__":
    main()
