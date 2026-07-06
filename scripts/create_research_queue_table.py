"""
Create conservative non-final property research queue.

Purpose:
- Turn valuation/context features into a human-review research queue.
- Preserve conservative interpretation rules.
- Prioritize properties for review without creating a final score.
- Do NOT create buy/sell recommendations.
- Do NOT call this an investment ranking.
- Do NOT backtest.

Input:
- data/interim/valuation_context_features.csv

Outputs:
- data/interim/property_research_queue.csv
- outputs/tables/property_research_queue_summary.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/interim/valuation_context_features.csv")
OUTPUT_PATH = Path("data/interim/property_research_queue.csv")
SUMMARY_PATH = Path("outputs/tables/property_research_queue_summary.csv")


HIGH_REVIEW_SIGNAL_COUNT = 2
MEDIUM_REVIEW_SIGNAL_COUNT = 1


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Ensure expected columns exist."""
    df = df.copy()

    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA

    return df


def parse_bool(value: object) -> bool:
    """Parse boolean-ish values safely."""
    if pd.isna(value):
        return False

    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()

    if text in {"true", "1", "yes", "y", "t"}:
        return True

    return False


def assign_research_priority(row: pd.Series) -> str:
    """Assign conservative research priority."""
    if row["candidate_review_bucket"] in {"reject", "hold"}:
        return "exclude_from_current_research_queue"

    if row["data_needs_review"]:
        return "needs_data_review_before_research"

    if row["valuation_context_signal_count"] >= HIGH_REVIEW_SIGNAL_COUNT:
        return "high_priority_human_review"

    if row["valuation_context_signal_count"] >= MEDIUM_REVIEW_SIGNAL_COUNT:
        return "medium_priority_human_review"

    if row["basic_price_context_available"]:
        return "low_priority_human_review"

    return "limited_context_watchlist"


def assign_research_queue_bucket(row: pd.Series) -> str:
    """Assign broad queue bucket."""
    priority = row["research_priority"]

    if priority == "high_priority_human_review":
        return "review_first"

    if priority == "medium_priority_human_review":
        return "review_next"

    if priority == "low_priority_human_review":
        return "review_if_time"

    if priority == "limited_context_watchlist":
        return "watchlist_limited_data"

    if priority == "needs_data_review_before_research":
        return "data_quality_review"

    return "excluded"


def build_research_reason(row: pd.Series) -> str:
    """Build concise human-readable research reason."""
    reasons: list[str] = []

    if row["below_home_type_median_ppsf"]:
        reasons.append("Price per sqft is below home-type median.")

    if row["far_below_home_type_median_ppsf"]:
        reasons.append("Price per sqft is far below home-type median.")

    if row["listing_price_below_zestimate_context"]:
        reasons.append("Listing price is below local Zestimate context.")

    if row["moderate_gross_rent_yield_context"]:
        reasons.append("Gross rent yield context is moderate or better.")

    if row["high_gross_rent_yield_context"]:
        reasons.append("Gross rent yield context is high.")

    if not reasons:
        reasons.append("No strong context signal yet; keep as low-confidence review item.")

    return " ".join(reasons)


def build_next_research_steps(row: pd.Series) -> str:
    """Build next human due-diligence steps."""
    steps = [
        "Verify current listing page manually.",
        "Confirm current asking price.",
        "Check property condition and listing description.",
        "Check HOA, taxes, insurance, and repair risk.",
        "Compare against recent nearby sold properties.",
    ]

    if not row["zestimate_available"]:
        steps.append("Pull or validate Zestimate separately if needed.")

    if not row["rent_zestimate_available"]:
        steps.append("Pull or validate Rent Zestimate separately if income context matters.")

    if row["data_needs_review"]:
        steps.append("Resolve data-quality flags before treating this as a research candidate.")

    return " ".join(steps)


def create_research_queue() -> pd.DataFrame:
    """Create conservative research queue."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}. Run Phase 14A first."
        )

    df = pd.read_csv(INPUT_PATH)

    required_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
        "home_status",
        "status_text",
        "candidate_state",
        "candidate_review_bucket",
        "eligible_for_context_features",
        "basic_price_context_available",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "home_type_count_for_ppsf_benchmark",
        "home_type_median_price_per_sqft",
        "price_per_sqft_vs_home_type_median_pct",
        "below_home_type_median_ppsf",
        "far_below_home_type_median_ppsf",
        "zestimate",
        "zestimate_available",
        "price_to_zestimate_pct",
        "zestimate_context_available",
        "listing_price_below_zestimate_context",
        "rent_zestimate",
        "rent_zestimate_available",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "income_context_available",
        "moderate_gross_rent_yield_context",
        "high_gross_rent_yield_context",
        "valuation_context_signal_count",
        "valuation_context_bucket",
        "context_confidence_notes",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "data_needs_review",
        "search_level_record_only",
        "detail_pull_completed",
        "overall_scoring_ready",
        "context_not_score",
        "valuation_score_created",
        "ranking_created",
        "buy_sell_recommendation_created",
        "zillow_url",
        "search_date",
        "data_source",
    ]

    df = ensure_columns(df, required_columns)

    numeric_columns = [
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "price_per_sqft",
        "home_type_count_for_ppsf_benchmark",
        "home_type_median_price_per_sqft",
        "price_per_sqft_vs_home_type_median_pct",
        "zestimate",
        "price_to_zestimate_pct",
        "rent_zestimate",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "valuation_context_signal_count",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    boolean_columns = [
        "eligible_for_context_features",
        "basic_price_context_available",
        "below_home_type_median_ppsf",
        "far_below_home_type_median_ppsf",
        "zestimate_available",
        "zestimate_context_available",
        "listing_price_below_zestimate_context",
        "rent_zestimate_available",
        "income_context_available",
        "moderate_gross_rent_yield_context",
        "high_gross_rent_yield_context",
        "outside_target_radius",
        "data_needs_review",
        "search_level_record_only",
        "detail_pull_completed",
        "overall_scoring_ready",
        "context_not_score",
        "valuation_score_created",
        "ranking_created",
        "buy_sell_recommendation_created",
    ]

    for column in boolean_columns:
        df[column] = df[column].apply(parse_bool)

    df["candidate_review_bucket"] = df["candidate_review_bucket"].fillna("hold")
    df["valuation_context_signal_count"] = df[
        "valuation_context_signal_count"
    ].fillna(0)

    df["research_priority"] = df.apply(assign_research_priority, axis=1)
    df["research_queue_bucket"] = df.apply(assign_research_queue_bucket, axis=1)
    df["research_reason"] = df.apply(build_research_reason, axis=1)
    df["next_research_steps"] = df.apply(build_next_research_steps, axis=1)

    # Conservative queue ordering only. This is not a final investment score.
    priority_order = {
        "high_priority_human_review": 1,
        "medium_priority_human_review": 2,
        "low_priority_human_review": 3,
        "limited_context_watchlist": 4,
        "needs_data_review_before_research": 5,
        "exclude_from_current_research_queue": 6,
    }

    df["research_priority_order"] = df["research_priority"].map(priority_order).fillna(99)

    df = df.sort_values(
        by=[
            "research_priority_order",
            "valuation_context_signal_count",
            "price_per_sqft_vs_home_type_median_pct",
        ],
        ascending=[True, False, True],
    ).reset_index(drop=True)

    df["research_queue_position"] = range(1, len(df) + 1)

    # Anti-overclaim safeguards.
    df["research_queue_not_investment_ranking"] = True
    df["final_score_created"] = False
    df["investment_recommendation_created"] = False
    df["buy_sell_recommendation_created"] = False
    df["backtesting_ready"] = False

    output_columns = [
        "research_queue_position",
        "research_priority",
        "research_queue_bucket",
        "research_reason",
        "next_research_steps",
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
        "home_status",
        "status_text",
        "candidate_state",
        "candidate_review_bucket",
        "eligible_for_context_features",
        "basic_price_context_available",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "home_type_count_for_ppsf_benchmark",
        "home_type_median_price_per_sqft",
        "price_per_sqft_vs_home_type_median_pct",
        "below_home_type_median_ppsf",
        "far_below_home_type_median_ppsf",
        "zestimate",
        "zestimate_available",
        "price_to_zestimate_pct",
        "listing_price_below_zestimate_context",
        "rent_zestimate",
        "rent_zestimate_available",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "moderate_gross_rent_yield_context",
        "high_gross_rent_yield_context",
        "valuation_context_signal_count",
        "valuation_context_bucket",
        "context_confidence_notes",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "data_needs_review",
        "search_level_record_only",
        "detail_pull_completed",
        "overall_scoring_ready",
        "research_queue_not_investment_ranking",
        "final_score_created",
        "investment_recommendation_created",
        "buy_sell_recommendation_created",
        "backtesting_ready",
        "zillow_url",
        "search_date",
        "data_source",
    ]

    df = ensure_columns(df, output_columns)

    return df[output_columns].copy()


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create research queue summary."""
    summary_rows = [
        {"metric": "total_records", "value": len(df)},
        {
            "metric": "review_first_count",
            "value": int((df["research_queue_bucket"] == "review_first").sum()),
        },
        {
            "metric": "review_next_count",
            "value": int((df["research_queue_bucket"] == "review_next").sum()),
        },
        {
            "metric": "review_if_time_count",
            "value": int((df["research_queue_bucket"] == "review_if_time").sum()),
        },
        {
            "metric": "watchlist_limited_data_count",
            "value": int((df["research_queue_bucket"] == "watchlist_limited_data").sum()),
        },
        {
            "metric": "data_quality_review_count",
            "value": int((df["research_queue_bucket"] == "data_quality_review").sum()),
        },
        {
            "metric": "excluded_count",
            "value": int((df["research_queue_bucket"] == "excluded").sum()),
        },
        {
            "metric": "final_score_created_count",
            "value": int(df["final_score_created"].sum()),
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

    summary = pd.DataFrame(summary_rows)

    bucket_summary = (
        df.groupby("research_queue_bucket", dropna=False)
        .size()
        .reset_index(name="value")
    )

    bucket_summary["metric"] = (
        "research_queue_bucket__" + bucket_summary["research_queue_bucket"].astype(str)
    )

    bucket_summary = bucket_summary[["metric", "value"]]

    home_type_summary = (
        df.groupby("home_type", dropna=False)
        .agg(
            record_count=("address", "count"),
            median_price=("price", "median"),
            median_price_per_sqft=("price_per_sqft", "median"),
            median_context_signal_count=("valuation_context_signal_count", "median"),
        )
        .reset_index()
    )

    home_type_summary["metric"] = (
        "home_type_summary__" + home_type_summary["home_type"].astype(str)
    )

    home_type_summary["value"] = home_type_summary.apply(
        lambda row: (
            f"records={row['record_count']}; "
            f"median_price={round(row['median_price'], 2) if pd.notna(row['median_price']) else 'NA'}; "
            f"median_ppsf={round(row['median_price_per_sqft'], 2) if pd.notna(row['median_price_per_sqft']) else 'NA'}; "
            f"median_context_signals={row['median_context_signal_count']}"
        ),
        axis=1,
    )

    home_type_summary = home_type_summary[["metric", "value"]]

    return pd.concat(
        [summary, bucket_summary, home_type_summary],
        ignore_index=True,
    )


def main() -> None:
    """Run Phase 15A."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    queue_df = create_research_queue()
    summary_df = create_summary(queue_df)

    queue_df.to_csv(OUTPUT_PATH, index=False)
    summary_df.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved research queue to: {OUTPUT_PATH}")
    print(f"Saved research queue summary to: {SUMMARY_PATH}")
    print()
    print("Important:")
    print("- This is a human-review research queue.")
    print("- This is not a final score.")
    print("- This is not an investment ranking.")
    print("- This is not a buy/sell recommendation.")
    print("- This is not backtesting-ready.")
    print()
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()