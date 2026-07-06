"""
Create conservative valuation/context feature table.

Purpose:
- Build cautious valuation and income context features from the active-listing
  candidate table.
- Compare listing price per square foot against local home-type medians.
- Preserve data-quality and candidate-gating fields.
- Create directional context signals only.

Important:
- This script does NOT create a final score.
- This script does NOT rank properties.
- This script does NOT make buy/sell recommendations.
- Zestimate and Rent Zestimate are treated as optional context only.

Inputs:
- data/interim/active_listing_candidate_table.csv

Outputs:
- data/interim/valuation_context_features.csv
- outputs/tables/valuation_context_feature_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


INPUT_PATH = Path("data/interim/active_listing_candidate_table.csv")
OUTPUT_PATH = Path("data/interim/valuation_context_features.csv")
SUMMARY_PATH = Path("outputs/tables/valuation_context_feature_summary.csv")


ELIGIBLE_REVIEW_BUCKETS = {"rankable_later", "needs_review"}

MIN_HOME_TYPE_GROUP_SIZE = 2

FAR_BELOW_MEDIAN_THRESHOLD = -0.10
BELOW_MEDIAN_THRESHOLD = -0.05

HIGH_GROSS_RENT_YIELD_THRESHOLD = 0.055
MODERATE_GROSS_RENT_YIELD_THRESHOLD = 0.045

ZESTIMATE_DISCOUNT_THRESHOLD = -0.03


def ensure_columns(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """Ensure required columns exist."""
    for column in required_columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def ensure_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to numeric if present."""
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def ensure_boolean(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Normalize boolean-ish columns."""
    true_values = {"true", "1", "yes", "y", "t"}
    false_values = {"false", "0", "no", "n", "f"}

    for column in columns:
        if column not in df.columns:
            df[column] = False
            continue

        def parse_bool(value: object) -> bool:
            if pd.isna(value):
                return False
            if isinstance(value, bool):
                return value
            text = str(value).strip().lower()
            if text in true_values:
                return True
            if text in false_values:
                return False
            return False

        df[column] = df[column].apply(parse_bool)

    return df


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Safely divide numeric pandas Series."""
    denominator = denominator.replace({0: pd.NA})
    return numerator / denominator


def create_home_type_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    """Create home-type median price-per-square-foot benchmarks."""
    eligible = df[
        (df["candidate_review_bucket"].isin(ELIGIBLE_REVIEW_BUCKETS))
        & (df["home_type"].notna())
        & (df["price_per_sqft"].notna())
        & (df["price_per_sqft"] > 0)
    ].copy()

    if eligible.empty:
        return pd.DataFrame(
            columns=[
                "home_type",
                "home_type_count_for_ppsf_benchmark",
                "home_type_median_price_per_sqft",
                "home_type_mean_price_per_sqft",
            ]
        )

    benchmarks = (
        eligible.groupby("home_type", dropna=False)
        .agg(
            home_type_count_for_ppsf_benchmark=("price_per_sqft", "count"),
            home_type_median_price_per_sqft=("price_per_sqft", "median"),
            home_type_mean_price_per_sqft=("price_per_sqft", "mean"),
        )
        .reset_index()
    )

    benchmarks["home_type_median_price_per_sqft"] = benchmarks[
        "home_type_median_price_per_sqft"
    ].round(2)

    benchmarks["home_type_mean_price_per_sqft"] = benchmarks[
        "home_type_mean_price_per_sqft"
    ].round(2)

    return benchmarks


def build_context_confidence_notes(row: pd.Series) -> str:
    """Build concise confidence note for each row."""
    notes: list[str] = []

    if row.get("candidate_review_bucket") in {"reject", "hold"}:
        notes.append("Not eligible for context due to candidate gating.")

    if not bool(row.get("basic_price_context_available", False)):
        notes.append("Basic price-per-square-foot context is limited or unavailable.")

    if bool(row.get("benchmark_group_too_small", False)):
        notes.append("Home-type benchmark group is too small.")

    if not bool(row.get("zestimate_available", False)):
        notes.append("Zestimate unavailable in local table.")

    if not bool(row.get("rent_zestimate_available", False)):
        notes.append("Rent Zestimate unavailable in local table.")

    if bool(row.get("search_level_record_only", True)):
        notes.append("Record remains search-level evidence only.")

    if not bool(row.get("detail_pull_completed", False)):
        notes.append("Detail pull not completed.")

    if not notes:
        notes.append("Basic context available; still not a score.")

    return " ".join(notes)


def assign_context_bucket(row: pd.Series) -> str:
    """Assign conservative valuation-context bucket."""
    if row.get("candidate_review_bucket") in {"reject", "hold"}:
        return "not_eligible_for_context"

    if not bool(row.get("basic_price_context_available", False)):
        return "limited_context"

    has_price = bool(row.get("basic_price_context_available", False))
    has_income = bool(row.get("income_context_available", False))
    has_zestimate = bool(row.get("zestimate_context_available", False))
    signal_count = row.get("valuation_context_signal_count", 0)

    if has_price and has_income and has_zestimate and signal_count >= 2:
        return "multi_signal_context_available"

    if has_price and has_income:
        return "price_and_income_context_available"

    if has_price and has_zestimate:
        return "price_and_zestimate_context_available"

    if has_price:
        return "basic_price_context_available"

    return "limited_context"


def create_valuation_context_features() -> pd.DataFrame:
    """Create valuation/context feature dataframe."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}. Run Phase 13A first."
        )

    df = pd.read_csv(INPUT_PATH)

    required_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "home_status",
        "status_text",
        "home_type",
        "fixture_classification",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "zestimate",
        "rent_zestimate",
        "price_to_zestimate_pct",
        "annual_rent_zestimate",
        "gross_rent_yield",
        "candidate_state",
        "candidate_review_bucket",
        "data_needs_review",
        "search_level_record_only",
        "detail_pull_completed",
        "overall_scoring_ready",
        "zillow_url",
        "search_date",
        "data_source",
    ]

    df = ensure_columns(df, required_columns)

    numeric_columns = [
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "price_per_sqft",
        "zestimate",
        "rent_zestimate",
        "price_to_zestimate_pct",
        "annual_rent_zestimate",
        "gross_rent_yield",
    ]

    boolean_columns = [
        "outside_target_radius",
        "data_needs_review",
        "search_level_record_only",
        "detail_pull_completed",
        "overall_scoring_ready",
    ]

    df = ensure_numeric(df, numeric_columns)
    df = ensure_boolean(df, boolean_columns)

    # Recalculate core derived metrics defensively.
    df["price_per_sqft"] = safe_divide(df["price"], df["square_feet"]).round(2)

    df["zestimate_available"] = df["zestimate"].notna() & (df["zestimate"] > 0)
    df["rent_zestimate_available"] = (
        df["rent_zestimate"].notna() & (df["rent_zestimate"] > 0)
    )

    df["annual_rent_zestimate"] = df["rent_zestimate"] * 12

    df["gross_rent_yield"] = safe_divide(
        df["annual_rent_zestimate"], df["price"]
    ).round(4)

    df["price_to_zestimate_pct"] = safe_divide(
        df["price"] - df["zestimate"], df["zestimate"]
    ).round(4)

    df["candidate_review_bucket"] = df["candidate_review_bucket"].fillna("hold")

    df["eligible_for_context_features"] = df["candidate_review_bucket"].isin(
        ELIGIBLE_REVIEW_BUCKETS
    )

    benchmarks = create_home_type_benchmarks(df)
    df = df.merge(benchmarks, on="home_type", how="left")

    df["home_type_count_for_ppsf_benchmark"] = pd.to_numeric(
        df["home_type_count_for_ppsf_benchmark"], errors="coerce"
    ).fillna(0)

    df["benchmark_group_too_small"] = (
        df["home_type_count_for_ppsf_benchmark"] < MIN_HOME_TYPE_GROUP_SIZE
    )

    df["price_per_sqft_vs_home_type_median_pct"] = safe_divide(
        df["price_per_sqft"] - df["home_type_median_price_per_sqft"],
        df["home_type_median_price_per_sqft"],
    ).round(4)

    df["basic_price_context_available"] = (
        df["eligible_for_context_features"]
        & df["price"].notna()
        & (df["price"] > 0)
        & df["square_feet"].notna()
        & (df["square_feet"] > 0)
        & df["price_per_sqft"].notna()
        & df["home_type_median_price_per_sqft"].notna()
        & ~df["benchmark_group_too_small"]
    )

    df["below_home_type_median_ppsf"] = (
        df["basic_price_context_available"]
        & (
            df["price_per_sqft_vs_home_type_median_pct"]
            <= BELOW_MEDIAN_THRESHOLD
        )
    )

    df["far_below_home_type_median_ppsf"] = (
        df["basic_price_context_available"]
        & (
            df["price_per_sqft_vs_home_type_median_pct"]
            <= FAR_BELOW_MEDIAN_THRESHOLD
        )
    )

    df["zestimate_context_available"] = (
        df["eligible_for_context_features"]
        & df["zestimate_available"]
        & df["price_to_zestimate_pct"].notna()
    )

    df["listing_price_below_zestimate_context"] = (
        df["zestimate_context_available"]
        & (df["price_to_zestimate_pct"] <= ZESTIMATE_DISCOUNT_THRESHOLD)
    )

    df["income_context_available"] = (
        df["eligible_for_context_features"]
        & df["rent_zestimate_available"]
        & df["gross_rent_yield"].notna()
    )

    df["moderate_gross_rent_yield_context"] = (
        df["income_context_available"]
        & (df["gross_rent_yield"] >= MODERATE_GROSS_RENT_YIELD_THRESHOLD)
    )

    df["high_gross_rent_yield_context"] = (
        df["income_context_available"]
        & (df["gross_rent_yield"] >= HIGH_GROSS_RENT_YIELD_THRESHOLD)
    )

    signal_columns = [
        "below_home_type_median_ppsf",
        "far_below_home_type_median_ppsf",
        "listing_price_below_zestimate_context",
        "moderate_gross_rent_yield_context",
        "high_gross_rent_yield_context",
    ]

    df["valuation_context_signal_count"] = df[signal_columns].sum(axis=1)

    df["valuation_context_bucket"] = df.apply(assign_context_bucket, axis=1)

    df["context_confidence_notes"] = df.apply(
        build_context_confidence_notes,
        axis=1,
    )

    # Explicit anti-overclaim flags.
    df["context_not_score"] = True
    df["valuation_score_created"] = False
    df["ranking_created"] = False
    df["buy_sell_recommendation_created"] = False

    output_columns = [
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
        "home_type_mean_price_per_sqft",
        "benchmark_group_too_small",
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

    df = ensure_columns(df, output_columns)

    return df[output_columns].copy()


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create valuation/context summary table."""
    required_summary_columns = [
        "eligible_for_context_features",
        "basic_price_context_available",
        "zestimate_context_available",
        "income_context_available",
        "below_home_type_median_ppsf",
        "far_below_home_type_median_ppsf",
        "listing_price_below_zestimate_context",
        "moderate_gross_rent_yield_context",
        "high_gross_rent_yield_context",
        "valuation_score_created",
        "ranking_created",
        "buy_sell_recommendation_created",
    ]

    df = ensure_columns(df.copy(), required_summary_columns)

    for column in required_summary_columns:
        df[column] = df[column].fillna(False).astype(bool)

    summary_rows = [
        {
            "metric": "total_records",
            "value": len(df),
        },
        {
            "metric": "eligible_for_context_features",
            "value": int(df["eligible_for_context_features"].sum()),
        },
        {
            "metric": "basic_price_context_available",
            "value": int(df["basic_price_context_available"].sum()),
        },
        {
            "metric": "zestimate_context_available",
            "value": int(df["zestimate_context_available"].sum()),
        },
        {
            "metric": "income_context_available",
            "value": int(df["income_context_available"].sum()),
        },
        {
            "metric": "below_home_type_median_ppsf",
            "value": int(df["below_home_type_median_ppsf"].sum()),
        },
        {
            "metric": "far_below_home_type_median_ppsf",
            "value": int(df["far_below_home_type_median_ppsf"].sum()),
        },
        {
            "metric": "listing_price_below_zestimate_context",
            "value": int(df["listing_price_below_zestimate_context"].sum()),
        },
        {
            "metric": "moderate_gross_rent_yield_context",
            "value": int(df["moderate_gross_rent_yield_context"].sum()),
        },
        {
            "metric": "high_gross_rent_yield_context",
            "value": int(df["high_gross_rent_yield_context"].sum()),
        },
        {
            "metric": "valuation_score_created",
            "value": int(df["valuation_score_created"].sum()),
        },
        {
            "metric": "ranking_created",
            "value": int(df["ranking_created"].sum()),
        },
        {
            "metric": "buy_sell_recommendation_created",
            "value": int(df["buy_sell_recommendation_created"].sum()),
        },
    ]

    summary = pd.DataFrame(summary_rows)

    if "valuation_context_bucket" in df.columns:
        bucket_summary = (
            df.groupby("valuation_context_bucket", dropna=False)
            .size()
            .reset_index(name="record_count")
        )

        bucket_summary["metric"] = (
            "valuation_context_bucket__"
            + bucket_summary["valuation_context_bucket"].astype(str)
        )

        bucket_summary = bucket_summary.rename(columns={"record_count": "value"})[
            ["metric", "value"]
        ]

        summary = pd.concat([summary, bucket_summary], ignore_index=True)

    if "home_type" in df.columns:
        home_type_summary = (
            df.groupby("home_type", dropna=False)
            .agg(
                record_count=("address", "count"),
                median_price=("price", "median"),
                median_price_per_sqft=("price_per_sqft", "median"),
                context_signal_count_sum=("valuation_context_signal_count", "sum"),
            )
            .reset_index()
        )

        home_type_summary["metric"] = (
            "home_type_summary__" + home_type_summary["home_type"].astype(str)
        )

        def format_home_type_summary(row: pd.Series) -> str:
            median_price = (
                round(row["median_price"], 2)
                if pd.notna(row["median_price"])
                else "NA"
            )
            median_ppsf = (
                round(row["median_price_per_sqft"], 2)
                if pd.notna(row["median_price_per_sqft"])
                else "NA"
            )
            return (
                f"records={row['record_count']}; "
                f"median_price={median_price}; "
                f"median_ppsf={median_ppsf}; "
                f"context_signals={row['context_signal_count_sum']}"
            )

        home_type_summary["value"] = home_type_summary.apply(
            format_home_type_summary,
            axis=1,
        )

        home_type_summary = home_type_summary[["metric", "value"]]

        summary = pd.concat([summary, home_type_summary], ignore_index=True)

    return summary


def main() -> None:
    """Run Phase 14A feature creation."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = create_valuation_context_features()
    summary = create_summary(df)

    df.to_csv(OUTPUT_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved valuation/context features to: {OUTPUT_PATH}")
    print(f"Saved valuation/context summary to: {SUMMARY_PATH}")
    print()
    print("Important:")
    print("- This is not a score.")
    print("- This is not a ranking.")
    print("- This is not a buy/sell recommendation.")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()