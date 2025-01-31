import streamlit as st
from retriever import retriever

def main():
    st.title("AI Recommendation Letter Generator")

    user_inputs = {}

    # Letter Type Selection
    lor_type = st.selectbox("Select Letter Type", ["immigration", "academic", "job"])

    # Dynamic Input Fields
    example_fields = {
        "immigration": ["applicant_name", "relationship", "field", "achievement"],
        "academic": ["applicant_name", "program", "course", "skill_1", "skill_2", "achievement"],
        "job": ["applicant_name", "position", "responsibility", "skill_1", "skill_2", "achievement"]
    }

    for field in example_fields[lor_type]:
        user_inputs[field] = st.text_input(label=field.replace('_', ' ').title())

    if st.button("Generate Letter"):
        result = retriever.generate_lor(user_inputs)
        st.subheader("Generated Letter")
        st.markdown(f"```\n{result}\n```")

if __name__ == "__main__":
    main()
