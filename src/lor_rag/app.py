"""Streamlit application for recommendation letter generation."""

from __future__ import annotations

import logging
import re

try:
    import streamlit as st
except ImportError:  # pragma: no cover - allows logic tests without streamlit installed
    st = None

LOGGER = logging.getLogger(__name__)


def extract_score(text: str) -> int:
    """Extract a heuristic score (1-10) from uploaded student details."""

    score = 0
    patterns = {
        "cgpa": r"CGPA[:\-]?\s*(\d\.\d+)",
        "achievements": r"achievement[:\-]?\s*(.+)",
        "skills": r"skills[:\-]?\s*(.+)",
        "research": r"research[:\-]?\s*(.+)",
    }

    # Weighted regex matching to map profile richness to recommendation strength.
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue

        score += 2
        if key == "cgpa":
            try:
                cgpa = float(match.group(1))
                if cgpa > 3.8:
                    score += 2
                elif cgpa > 3.5:
                    score += 1
            except ValueError:
                LOGGER.warning("Unable to parse CGPA from uploaded text.")

    return min(10, max(1, score))


def lor_level(rating: int) -> str:
    """Map a numeric rating to a recommendation level label."""

    if rating >= 9:
        return "high"
    if rating >= 7:
        return "medium-high"
    if rating >= 5:
        return "medium"
    if rating >= 3:
        return "medium-low"
    return "low"


def main() -> None:
    """Render and run the Streamlit app."""

    if st is None:
        raise RuntimeError("streamlit is required to run the UI app.")

    from .generator import LORGenerator
    from .indexer import LORIndexer

    st.title("LOR Generator")

    st.markdown(
        """
        <style>
            div[data-testid="stFileUploader"] section div {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    file_upload = st.file_uploader("Upload Student Information", type=["txt"])

    if file_upload is None:
        return

    user_text = file_upload.read().decode("utf-8")
    st.text_area("Uploaded text", user_text, height=200)

    try:
        indexer = LORIndexer()
        _, similar_score = indexer.search_match(user_text)
    except Exception as exc:  # pragma: no cover - streamlit runtime path
        LOGGER.exception("Failed to process FAISS index")
        st.error(f"Could not process templates: {exc}")
        return

    extracted_rating = extract_score(user_text)
    final_rating = (extracted_rating + similar_score) // 2
    predicted_level = lor_level(final_rating)

    st.subheader("LOR Analysis:")
    st.write(f"Extracted Rating: **{extracted_rating}/10**")
    st.write(f"Similarity Score Rating: **{similar_score}/10**")
    st.write(f"Final Predicted Rating: **{final_rating}/10**")
    st.write(f"Suggested LOR Level: **{predicted_level.capitalize()}**")

    level_options = ["high", "medium-high", "medium", "medium-low", "low", "dont-provide"]
    selected_level = st.selectbox(
        "Select LOR Level",
        level_options,
        index=level_options.index(predicted_level),
    )

    if selected_level == "dont-provide":
        st.write("You should not provide an LOR.")
        return

    if st.button("Generate LOR"):
        generator = LORGenerator()
        generated_lor = generator.generate_lor(user_text, selected_level)
        st.subheader("Generated Letter of Recommendation:")
        st.text_area("", generated_lor, height=500)
