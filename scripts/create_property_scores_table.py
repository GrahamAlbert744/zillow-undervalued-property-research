"""
Create the conservative MVP research-ranking score table (Decision 019).

Purpose:
- Apply src/scoring.py's 100-point framework (40/25/20/15) to every
  property already past candidate gating (Decision 013).
- Score is a research-ranking signal only, not a final valuation and not a
  buy/sell/investment recommendation (see docs/scoring_methodology.md).
- Missing data reduces the achievable score; it never inflates it
  (Decision 005).

Runs after scripts/create_valuation_context_features.py and before
scripts/create_research_queue_table.py in the pipeline order.

Input:
- data/interim/valuation_context_features.csv

Outputs:
- data/interim/property_scores.csv
- outputs/tables/undervaluation_scores_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.scoring import MAX_ACHIEVABLE_SCORE, score_property  # noqa: E402


INPUT_PATH = Path("data/interim/valuation_context_features.csv")
OUTPUT_PATH = Path("data/interim/property_scores.csv")
SUMMARY_PATH = Path("outputs/tables/undervaluation_scores_summary.csv")

# Only score properties already past candidate gating (Decision 013).
# reject/hold properties stay visible in candidate_exclusion_review_table.csv
# instead of being scored.
SCORE_ELIGIBLE_BUCKETS = {"rankable_later", "needs_review"}


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Ensure expected columns exist."""
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def create_property_scores() -> pd.DataFrame:
    """Score every candidate-gated property and attach score columns."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}. "
            "Run scripts/create_valuation_context_features.py first."
        )

    df = pd.read_csv(INPUT_PATH)

    df["candidate_review_bucket"] = df["candidate_review_bucket"].fillna("hold")
    df["score_eligible"] = df["candidate_review_bucket"].isin(SCORE_ELIGIBLE_BUCKETS)

    score_columns = [
        "valuation_score",
        "income_potential_score",
        "property_usefulness_score",
        "data_quality_score",
        "total_research_score",
        "max_achievable_research_score",
        "score_confidence_notes",
    ]

    for column in score_columns:
        df[column] = pd.NA

    for index, row in df.iterrows():
        if not bool(row["score_eligible"]):
            df.at[index, "score_confidence_notes"] = (
                "Not scored: excluded by candidate gating "
                f"(candidate_review_bucket={row['candidate_review_bucket']}). "
                "See candidate_exclusion_review_table.csv for the reason."
            )
            continue

        result = score_property(row.to_dict())
        for column in score_columns:
            df.at[index, column] = result[column]

    df["research_score_created"] = df["score_eligible"]

    # Explicit anti-overclaim flags — scoring is now in scope (Decision 019),
    # but none of the following are, and this script must never set them.
    df["fair_value_estimate_created"] = False
    df["investment_recommendation_created"] = False
    df["buy_sell_recommendation_created"] = False
    df["backtesting_ready"] = False

    output_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
        "candidate_review_bucket",
        "score_eligible",
        "research_score_created",
        "valuation_score",
        "income_potential_score",
        "property_usefulness_score",
        "data_quality_score",
        "total_research_score",
        "max_achievable_research_score",
        "score_confidence_notes",
        "fair_value_estimate_created",
        "investment_recommendation_created",
        "buy_sell_recommendation_created",
        "backtesting_ready",
    ]

    df = ensure_columns(df, output_columns)

    # Keep every original column too, so downstream stages (research queue)
    # can consume the score alongside the existing context features without
    # a second merge back to valuation_context_features.csv.
    remaining_columns = [column for column in df.columns if column not in output_columns]
    ordered_columns = output_columns + remaining_columns

    return df[ordered_columns].copy()


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create scoring summary table."""
    scored = df[df["research_score_created"] == True]  # noqa: E712

    summary_rows = [
        {"metric": "total_records", "value": len(df)},
        {"metric": "scored_records", "value": len(scored)},
        {
            "metric": "not_scored_excluded_by_candidate_gating",
            "value": int((~df["score_eligible"]).sum()),
        },
        {
            "metric": "max_achievable_research_score",
            "value": MAX_ACHIEVABLE_SCORE,
        },
        {
            "metric": "fair_value_estimate_created_count",
            "value": int(df["fair_value_estimate_created"].sum()),
        },
        {
            "metric": "investment_recommendation_created_count",
            "value": int(df["investment_recommendation_created"].sum()),
        },
        {
            "metric": "buy_sell_recommendation_created_count",
            "value": int(df["buy_sell_recommendation_created"].sum()),
        },
        {
            "metric": "backtesting_ready_count",
            "value": int(df["backtesting_ready"].sum()),
        },
    ]

    if len(scored) > 0:
        summary_rows.extend(
            [
                {
                    "metric": "median_total_research_score",
                    "value": round(float(scored["total_research_score"].median()), 2),
                },
                {
                    "metric": "max_total_research_score_observed",
                    "value": round(float(scored["total_research_score"].max()), 2),
                },
                {
                    "metric": "min_total_research_score_observed",
                    "value": round(float(scored["total_research_score"].min()), 2),
                },
            ]
        )

    return pd.DataFrame(summary_rows)


def main() -> None:
    """Run the scoring stage."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = create_property_scores()
    summary = create_summary(df)

    df.to_csv(OUTPUT_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved property scores to: {OUTPUT_PATH}")
    print(f"Saved scoring summary to: {SUMMARY_PATH}")
    print()
    print("Important:")
    print("- This is a research-ranking score, not a final valuation.")
    print("- This is not an investment recommendation.")
    print("- This is not a purchase or sale recommendation.")
    print("- This is not backtesting-ready.")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
