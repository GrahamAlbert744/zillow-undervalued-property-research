"""
Create candidate exclusion / hold review table.

Purpose:
- Make properties excluded or held at the candidate-gating stage visible,
  not silently dropped.
- Explain why each property was rejected, held, or flagged for review.
- Distinguish reject from hold from needs_review.
- Cross-reference the research queue's disposition for the same property_id.
- Do NOT score excluded records.
- Do NOT treat missing data as false attractiveness or as a zero score.
- Do NOT create a final valuation or investment ranking.

Inputs:
- data/interim/active_listing_candidate_table.csv
- data/interim/property_research_queue.csv (optional cross-reference)

Outputs:
- data/interim/candidate_exclusion_review_table.csv
- outputs/tables/candidate_exclusion_review_summary.csv
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.output_labels import label_for_exclusion_type  # noqa: E402


CANDIDATE_INPUT_PATH = Path("data/interim/active_listing_candidate_table.csv")
QUEUE_INPUT_PATH = Path("data/interim/property_research_queue.csv")
OUTPUT_PATH = Path("data/interim/candidate_exclusion_review_table.csv")
SUMMARY_PATH = Path("outputs/tables/candidate_exclusion_review_summary.csv")


EXCLUDED_REVIEW_BUCKETS = {"reject", "hold", "needs_review"}


def build_exclusion_reason_summary(row: pd.Series) -> str:
    """Explain, in plain language, why this property was excluded or held."""
    reasons: list[str] = []

    if row["missing_price"]:
        reasons.append("Missing price.")

    if row["invalid_price"]:
        reasons.append("Invalid price (<= 0).")

    if row["outside_target_radius"] is True:
        reasons.append("Outside the 25-mile target radius.")

    if row["is_residential_property"] is False:
        reasons.append("Non-residential property type.")

    if row["missing_square_feet"]:
        reasons.append("Missing square footage.")

    if row["invalid_square_feet"]:
        reasons.append("Invalid square footage (<= 0).")

    if row["missing_home_type"]:
        reasons.append("Missing home type.")

    if row["missing_lat_long"]:
        reasons.append("Missing latitude/longitude.")

    if row["missing_beds"] or row["missing_baths"]:
        reasons.append("Missing core bed/bath details.")

    if row["undisclosed_address"]:
        reasons.append("Address undisclosed by listing source.")

    if row["suspiciously_low_price_per_sqft"]:
        reasons.append("Suspiciously low price per square foot.")

    if row["suspiciously_high_price_per_sqft"]:
        reasons.append("Suspiciously high price per square foot.")

    if not reasons and row["data_needs_review"]:
        reasons.append("Flagged for data-quality review.")

    if not reasons:
        reasons.append(
            "Held or flagged for manual review; no single hard-gate failure identified."
        )

    return " ".join(reasons)


def build_next_review_step(exclusion_type: str) -> str:
    """Describe the conservative next step for this review bucket."""
    if exclusion_type == "reject":
        return (
            "No action planned unless corrected source data becomes available "
            "(e.g., a re-pull with a valid price or residential property type)."
        )

    if exclusion_type == "hold":
        return (
            "Re-run the pipeline after missing core fields (square footage, "
            "geography, home type, beds/baths) become available."
        )

    return "Manually confirm listing details before treating this as a research candidate."


def create_exclusion_review_table() -> pd.DataFrame:
    """Create the candidate exclusion / hold review table."""
    if not CANDIDATE_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {CANDIDATE_INPUT_PATH}. "
            "Run scripts/create_active_listing_candidate_table.py first."
        )

    candidate_df = pd.read_csv(CANDIDATE_INPUT_PATH)

    boolean_columns = [
        "is_residential_property",
        "outside_target_radius",
        "missing_price",
        "missing_square_feet",
        "missing_beds",
        "missing_baths",
        "missing_home_type",
        "missing_lat_long",
        "undisclosed_address",
        "invalid_price",
        "invalid_square_feet",
        "suspiciously_low_price_per_sqft",
        "suspiciously_high_price_per_sqft",
        "data_needs_review",
    ]

    for column in boolean_columns:
        if column not in candidate_df.columns:
            candidate_df[column] = False
        candidate_df[column] = candidate_df[column].apply(
            lambda value: bool(value) if pd.notna(value) else False
        )

    df = candidate_df[
        candidate_df["candidate_review_bucket"].isin(EXCLUDED_REVIEW_BUCKETS)
    ].copy()

    df["exclusion_type"] = df["candidate_review_bucket"]
    # CLAUDE.md-compliant display label (Decision 020).
    df["conservative_output_label"] = df["exclusion_type"].apply(label_for_exclusion_type)
    df["exclusion_reason_summary"] = df.apply(build_exclusion_reason_summary, axis=1)
    df["next_review_step"] = df["exclusion_type"].apply(build_next_review_step)

    if QUEUE_INPUT_PATH.exists():
        queue_df = pd.read_csv(
            QUEUE_INPUT_PATH,
            usecols=["property_id", "research_queue_bucket", "research_priority"],
        )
        queue_df = queue_df.rename(
            columns={
                "research_queue_bucket": "queue_cross_reference_bucket",
                "research_priority": "queue_cross_reference_priority",
            }
        )
        df = df.merge(queue_df, on="property_id", how="left")
    else:
        df["queue_cross_reference_bucket"] = pd.NA
        df["queue_cross_reference_priority"] = pd.NA

    # Anti-overclaim safeguards. This table explains exclusions; it does not score them.
    df["candidate_exclusion_review_not_final"] = True
    df["records_silently_dropped"] = False
    df["exclusion_score_created"] = False

    output_columns = [
        "property_id",
        "zpid",
        "address",
        "city",
        "state",
        "zip_code",
        "home_type",
        "is_residential_property",
        "price",
        "beds",
        "baths",
        "square_feet",
        "lot_size",
        "lot_size_units",
        "price_per_sqft",
        "latitude",
        "longitude",
        "distance_from_02131_miles",
        "outside_target_radius",
        "candidate_state",
        "candidate_review_bucket",
        "exclusion_type",
        "conservative_output_label",
        "exclusion_reason_summary",
        "missing_price",
        "invalid_price",
        "missing_square_feet",
        "invalid_square_feet",
        "missing_home_type",
        "missing_lat_long",
        "missing_beds",
        "missing_baths",
        "undisclosed_address",
        "suspiciously_low_price_per_sqft",
        "suspiciously_high_price_per_sqft",
        "data_needs_review",
        "queue_cross_reference_bucket",
        "queue_cross_reference_priority",
        "next_review_step",
        "zillow_url",
        "search_date",
        "data_source",
        "candidate_exclusion_review_not_final",
        "records_silently_dropped",
        "exclusion_score_created",
    ]

    for column in output_columns:
        if column not in df.columns:
            df[column] = pd.NA

    return df[output_columns].reset_index(drop=True)


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create exclusion/hold review summary."""
    rows = [
        {"metric": "records_in_exclusion_review_table", "value": len(df)},
        {
            "metric": "reject_count",
            "value": int((df["exclusion_type"] == "reject").sum()),
        },
        {
            "metric": "hold_count",
            "value": int((df["exclusion_type"] == "hold").sum()),
        },
        {
            "metric": "needs_review_count",
            "value": int((df["exclusion_type"] == "needs_review").sum()),
        },
        {
            "metric": "missing_price_count",
            "value": int(df["missing_price"].sum()),
        },
        {
            "metric": "outside_target_radius_count",
            "value": int(df["outside_target_radius"].fillna(False).sum()),
        },
        {
            "metric": "missing_square_feet_count",
            "value": int(df["missing_square_feet"].sum()),
        },
        {
            "metric": "missing_lat_long_count",
            "value": int(df["missing_lat_long"].sum()),
        },
        {
            "metric": "undisclosed_address_count",
            "value": int(df["undisclosed_address"].sum()),
        },
        {
            "metric": "data_needs_review_count",
            "value": int(df["data_needs_review"].sum()),
        },
    ]

    summary = pd.DataFrame(rows)

    reason_counts = (
        df["exclusion_type"]
        .value_counts(dropna=False)
        .rename_axis("exclusion_type")
        .reset_index(name="value")
    )
    reason_counts["metric"] = "exclusion_type__" + reason_counts["exclusion_type"].astype(str)
    reason_counts = reason_counts[["metric", "value"]]

    # CLAUDE.md-compliant label counts (Decision 020), additive alongside
    # the internal exclusion_type counts above.
    label_counts = (
        df["conservative_output_label"]
        .value_counts(dropna=False)
        .rename_axis("conservative_output_label")
        .reset_index(name="value")
    )
    label_counts["metric"] = (
        "conservative_output_label__" + label_counts["conservative_output_label"].astype(str)
    )
    label_counts = label_counts[["metric", "value"]]

    return pd.concat([summary, reason_counts, label_counts], ignore_index=True)


def main() -> None:
    """Create candidate exclusion / hold review outputs."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    exclusion_df = create_exclusion_review_table()
    summary_df = create_summary(exclusion_df)

    exclusion_df.to_csv(OUTPUT_PATH, index=False)
    summary_df.to_csv(SUMMARY_PATH, index=False)

    print(f"Saved candidate exclusion review table to: {OUTPUT_PATH}")
    print(f"Saved candidate exclusion review summary to: {SUMMARY_PATH}")
    print()
    print("Important:")
    print("- Excluded and held properties are preserved here, not dropped.")
    print("- This table explains exclusions; it does not score them.")
    print("- This is not a final valuation or investment ranking.")
    print()
    print(summary_df.to_string(index=False))
    print()
    print("Preview:")
    print(
        exclusion_df[
            [
                "address",
                "home_type",
                "candidate_state",
                "exclusion_type",
                "exclusion_reason_summary",
            ]
        ].head(20).to_string(index=False)
    )


if __name__ == "__main__":
    main()
