import streamlit as st
from database import get_recommendation_history

st.set_page_config(
    page_title="Recommendation History",
    layout="wide"
)

st.title("📜 Recommendation History")

df = get_recommendation_history()

# Search Box
search = st.text_input("🔍 Search Workflow")

if search:
    df = df[
        df["RecommendedWorkflow"]
        .str.contains(search, case=False, na=False)
    ]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Download CSV
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download History",
    data=csv,
    file_name="RecommendationHistory.csv",
    mime="text/csv"
)