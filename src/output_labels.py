"""
Conservative output labels for the Zillow undervalued-property project
(Decision 020).

Purpose:
- CLAUDE.md restricts human-facing output labels to exactly five strings
  (see Decision 003): "research first", "watchlist", "avoid",
  "possible candidate after human review", "needs data review".
- The pipeline's internal bucket vocabulary (research_queue_bucket,
  candidate_review_bucket, exclusion_type) was never mapped onto those
  five strings anywhere — Decision 019 flagged this gap without closing
  it. This module closes it additively: it does not rename or change any
  internal bucket, it only derives a display label from one.

This module does not decide which bucket a property falls into. That
remains entirely the job of scripts/create_research_queue_table.py and
scripts/create_candidate_exclusion_review_table.py.
"""

from __future__ import annotations

# The only five labels CLAUDE.md permits anywhere in this project's output.
ALLOWED_OUTPUT_LABELS = {
    "research first",
    "watchlist",
    "avoid",
    "possible candidate after human review",
    "needs data review",
}

# Maps scripts/create_research_queue_table.py's research_queue_bucket
# values onto the allowed labels.
#
# - review_first -> "research first": the clearest one-to-one fit.
# - review_next -> "possible candidate after human review": medium
#   priority, still scoring-eligible, but not the top tier.
# - review_if_time / watchlist_limited_data -> "watchlist": both are
#   lower-priority-but-not-disqualified.
# - data_quality_review -> "needs data review": exact semantic match.
# - excluded -> "avoid": hard-filtered by candidate gating (outside
#   radius, non-residential, invalid core data). This means "doesn't meet
#   the project's basic research criteria," not an investment judgment,
#   and a data problem never inflates this label upward (Decision 005).
QUEUE_BUCKET_TO_LABEL: dict[str, str] = {
    "review_first": "research first",
    "review_next": "possible candidate after human review",
    "review_if_time": "watchlist",
    "watchlist_limited_data": "watchlist",
    "data_quality_review": "needs data review",
    "excluded": "avoid",
}

# Maps scripts/create_candidate_exclusion_review_table.py's exclusion_type
# values (mirrored from candidate_review_bucket) onto the allowed labels.
#
# - reject -> "avoid": fails a hard eligibility filter.
# - hold / needs_review -> "needs data review": both are explicitly
#   recoverable once more/better data is available.
EXCLUSION_TYPE_TO_LABEL: dict[str, str] = {
    "reject": "avoid",
    "hold": "needs data review",
    "needs_review": "needs data review",
}


def assert_valid_label(label: str) -> str:
    """
    Raise ValueError if label is not one of the five CLAUDE.md-allowed
    output labels. Returns the label unchanged otherwise, so this can be
    used inline.
    """
    if label not in ALLOWED_OUTPUT_LABELS:
        raise ValueError(
            f"{label!r} is not an allowed output label. CLAUDE.md restricts "
            f"output labels to: {sorted(ALLOWED_OUTPUT_LABELS)}."
        )
    return label


def label_for_queue_bucket(research_queue_bucket: str) -> str:
    """Return the conservative output label for a research_queue_bucket value."""
    label = QUEUE_BUCKET_TO_LABEL.get(research_queue_bucket)
    if label is None:
        raise ValueError(
            f"No conservative_output_label mapping for research_queue_bucket "
            f"{research_queue_bucket!r}. Add it to QUEUE_BUCKET_TO_LABEL."
        )
    return assert_valid_label(label)


def label_for_exclusion_type(exclusion_type: str) -> str:
    """Return the conservative output label for an exclusion_type value."""
    label = EXCLUSION_TYPE_TO_LABEL.get(exclusion_type)
    if label is None:
        raise ValueError(
            f"No conservative_output_label mapping for exclusion_type "
            f"{exclusion_type!r}. Add it to EXCLUSION_TYPE_TO_LABEL."
        )
    return assert_valid_label(label)
