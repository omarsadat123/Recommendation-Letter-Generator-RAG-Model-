from __future__ import annotations

import re

import streamlit as st

from lor_generator import LORGenerator
from lor_indexer import LORIndexer

st.set_page_config(page_title="LOR Generator", page_icon="📝", layout="wide")


def extract_score(text: str) -> int:
    score = 0
    patterns = {
        "cgpa": r"CGPA[:\-]?\s*(\d(?:\.\d+)?)",
        "achievements": r"achievement[:\-]?\s*(.+)",
        "skills": r"skills[:\-]?\s*(.+)",
        "research": r"research[:\-]?\s*(.+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score += 2
            if key == "cgpa":
                try:
                    cgpa = float(match.group(1))
                    if cgpa >= 3.8:
                        score += 2
                    elif cgpa >= 3.5:
                        score += 1
                except ValueError:
                    pass

    return min(10, max(1, score))


def lor_level(rating: int) -> str:
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
    st.title("📝 Recommendation Letter Generator")
    st.caption("Upload a student profile, review the score, and generate a polished LOR.")

    uploaded_file = st.file_uploader("Upload Student Information", type=["txt"])

    if uploaded_file is None:
        st.info("Upload a text file to begin.")
        return

    user_text = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded text", user_text, height=220)

    indexer = LORIndexer()
    match_index, similarity_score = indexer.search_match(user_text)

    extracted_rating = extract_score(user_text)
    final_rating = round((extracted_rating + similarity_score) / 2)
    predicted_level = lor_level(final_rating)

    st.subheader("LOR Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Extracted Rating", f"{extracted_rating}/10")
    col2.metric("Similarity Rating", f"{similarity_score}/10")
    col3.metric("Final Rating", f"{final_rating}/10")
    st.write(f"**Suggested LOR Level:** {predicted_level.replace('-', ' ').title()}")

    level_options = ["high", "medium-high", "medium", "medium-low", "low", "dont-provide"]
    selected_level = st.selectbox(
        "Select LOR Level",
        level_options,
        index=level_options.index(predicted_level),
        format_func=lambda x: "Do not provide LOR" if x == "dont-provide" else x.replace("-", " ").title(),
    )

    if selected_level == "dont-provide":
        st.warning("You should not provide an LOR.")
        return

    if st.button("Generate LOR", type="primary"):
        with st.spinner("Generating letter..."):
            generator = LORGenerator()
            generated_lor = generator.generate_lor(user_text, selected_level)

        st.subheader("Generated Letter of Recommendation")
        st.text_area("", generated_lor, height=520)

        st.download_button(
            label="Download LOR",
            data=generated_lor,
            file_name="generated_lor.txt",
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
