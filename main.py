import streamlit as st
from lor_indexer import LORIndexer
from lor_generator import LORGenerator
import re

# extract details and calculate rating
def extract_score(text):
    score = 0
    patterns = {
        "cgpa": r"CGPA[:\-]?\s*(\d\.\d+)",
        "achievements": r"achievement[:\-]?\s*(.+)",
        "skills": r"skills[:\-]?\s*(.+)",
        "research": r"research[:\-]?\s*(.+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score += 2
            if key == "cgpa":
                try:
                    cgpa = float(match.group(1))
                    if cgpa > 3.8:
                        score += 2
                    elif cgpa > 3.5:
                        score += 1
                except ValueError:
                    pass

    return min(10, max(1, score))

# LOR level based on rating
def lor_level(rating):
    if rating >= 9:
        return "high"
    elif rating >= 7:
        return "medium-high"
    elif rating >= 5:
        return "medium"
    elif rating >= 3:
        return "medium-low"
    else:
        return "low"

def main():
    st.title("LOR Generator")
    
    st.markdown(
        """
        <style>
            div[data-testid="stFileUploader"] section div { 
                display: none !important; 
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    File_upload = st.file_uploader("Upload Student Information", type=["txt"])
    
    if File_upload is not None:
        user_text = File_upload.read().decode("utf-8")
        st.text_area("Uploaded text", user_text, height=200)

        
        indexer = LORIndexer()      # Load FAISS indexer
        match_idex, similar_score = indexer.search_match(user_text)

        
        extracted_rating = extract_score(user_text)                      # Extract rating and final score
        final_rating = (extracted_rating + similar_score) // 2

       
        predicted_level = lor_level(final_rating)      # Calculate rating

        st.subheader("LOR Analysis:")
        st.write(f"Extracted Rating: **{extracted_rating}/10**")
        st.write(f"Similarity Score Rating: **{similar_score}/10**")
        st.write(f"Final Predicted Rating: **{final_rating}/10**")
        st.write(f"Suggested LOR Level: **{predicted_level.capitalize()}**")

        # select level
        level_options = ["high", "medium-high", "medium", "medium-low", "low", "dont-provide"]
        selected_level = st.selectbox("Select LOR Level", level_options, index=level_options.index(predicted_level))

        if selected_level != "dont-provide" and st.button("Generate LOR"):
            generator = LORGenerator()
            generated_lor = generator.generate_lor(user_text, selected_level)
            st.subheader("Generated Letter of Recommendation:")
            st.text_area("", generated_lor, height=500)
        elif selected_level == "dont-provide":
            st.write("You should not provide an LOR.")

if __name__ == "__main__":
    main()
