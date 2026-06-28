import streamlit as st
import plotly.express as px
import pandas as pd

from database import (
    get_dashboard_data,
    get_recommendation_history
)

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------------

st.markdown("""

<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:2rem;
}

.title{
    font-size:42px;
    font-weight:bold;
    color:#1E3A8A;
}

.subtitle{
    font-size:18px;
    color:#666666;
}

.metric-card{

    background:white;

    border-radius:15px;

    padding:18px;

    box-shadow:0px 4px 10px rgba(0,0,0,.08);

    border-left:8px solid #2563EB;

    text-align:center;

}

.metric-title{

    color:gray;

    font-size:15px;

}

.metric-value{

    font-size:36px;

    font-weight:bold;

    color:#111827;

}

.section{

    background:white;

    border-radius:15px;

    padding:20px;

    box-shadow:0px 4px 10px rgba(0,0,0,.06);

    margin-top:20px;

}

</style>

""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

try:

    total_req,total_rec,avg_conf,generated = get_dashboard_data()

    df = get_recommendation_history()

except Exception as e:

    st.error(e)

    st.stop()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown(
"""
<div class='title'>

🤖 Enterprise AI Executive Dashboard

</div>

<div class='subtitle'>

AI Powered Requirement Analysis & Recommendation Platform

</div>

""",

unsafe_allow_html=True

)

st.write("")

# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

📋 Requirements

</div>

<div class="metric-value">

{total_req}

</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

🤖 Recommendations

</div>

<div class="metric-value">

{total_rec}

</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

🎯 Avg Confidence

</div>

<div class="metric-value">

{avg_conf:.1f}%

</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

✅ Reports

</div>

<div class="metric-value">

{generated}

</div>

</div>

""",unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------
# CHARTS
# -------------------------------------------------------

st.subheader("📊 Analytics")

col1, col2 = st.columns(2)

# ==========================================
# Workflow Usage
# ==========================================

with col1:

    st.markdown("### 🔄 Workflow Usage")

    workflow_counts = (
        df["RecommendedWorkflow"]
        .value_counts()
        .reset_index()
    )

    workflow_counts.columns = [
        "Workflow",
        "Count"
    ]

    fig = px.bar(
        workflow_counts,
        x="Count",
        y="Workflow",
        orientation="h",
        color="Count",
        text="Count",
        color_continuous_scale="Blues"
    )

    fig.update_layout(

        height=420,

        xaxis_title="Recommendations",

        yaxis_title="",

        template="plotly_white",

        coloraxis_showscale=False,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# Recommendation Status
# ==========================================

with col2:

    st.markdown("### ✅ Recommendation Status")

    status_counts = (
        df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig2 = px.bar(

        status_counts,

        x="Status",

        y="Count",

        color="Status",

        text="Count"

    )

    fig2.update_layout(

        template="plotly_white",

        height=420,

        showlegend=False,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------------
# AI INSIGHTS
# -------------------------------------------------------

st.subheader("🧠 AI Insights")

left, right = st.columns([2, 1])

with left:

    top_workflow = df["RecommendedWorkflow"].mode()[0]

    latest = df.iloc[0]

    st.success(f"""
### Top Recommended Workflow

**{top_workflow}**

This workflow is currently the most frequently recommended by the AI engine.
""")

    st.info(f"""
### Latest Recommendation

Workflow : **{latest['RecommendedWorkflow']}**

Status : **{latest['Status']}**

Confidence : **{latest['ConfidenceScore']}%**
""")

with right:

    st.metric(
        "🎯 Average Confidence",
        f"{df['ConfidenceScore'].mean():.1f}%"
    )

    st.metric(
        "📄 Total Recommendations",
        len(df)
    )

st.divider()

# -------------------------------------------------------
# RECENT ACTIVITY
# -------------------------------------------------------

st.subheader("📅 Recent Activity")

activity = df.copy()

activity = activity[[
    "RecommendationDate",
    "RecommendedWorkflow",
    "Status",
    "ConfidenceScore"
]]

activity.columns = [
    "Date",
    "Workflow",
    "Status",
    "Confidence %"
]

st.dataframe(
    activity.head(10),
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------------
# FILTERS
# -------------------------------------------------------

st.subheader("🔍 Search & Filter")

col1, col2 = st.columns(2)

with col1:
    search = st.text_input(
        "Search Workflow",
        placeholder="Type workflow name..."
    )

with col2:
    status_filter = st.selectbox(
        "Filter Status",
        ["All"] + sorted(df["Status"].unique().tolist())
    )

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["RecommendedWorkflow"]
        .str.contains(search, case=False, na=False)
    ]

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Status"] == status_filter
    ]

st.divider()

# -------------------------------------------------------
# TOP WORKFLOWS
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top Workflows")

    top = (
        filtered_df["RecommendedWorkflow"]
        .value_counts()
        .head(5)
        .reset_index()
    )

    top.columns = [
        "Workflow",
        "Recommendations"
    ]

    fig3 = px.bar(
        top,
        x="Recommendations",
        y="Workflow",
        orientation="h",
        color="Recommendations",
        text="Recommendations",
        color_continuous_scale="Viridis"
    )

    fig3.update_layout(
        template="plotly_white",
        height=400,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# -------------------------------------------------------
# CONFIDENCE DISTRIBUTION
# -------------------------------------------------------

with right:

    st.subheader("🎯 Confidence Distribution")

    fig4 = px.histogram(
        filtered_df,
        x="ConfidenceScore",
        nbins=10,
        color_discrete_sequence=["#2563EB"]
    )

    fig4.update_layout(
        template="plotly_white",
        height=400,
        xaxis_title="Confidence %",
        yaxis_title="Recommendations",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------------
# RECOMMENDATION HISTORY
# -------------------------------------------------------

st.subheader("📜 Recommendation History")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download Recommendation History (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="recommendation_history.csv",
    mime="text/csv"
)

st.divider()

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown(
"""
---
<center>

### 🤖 Enterprise AI Recommendation Engine

Built with **Streamlit + SQL Server + Ollama (Llama 3.2)**

</center>
""",
unsafe_allow_html=True
)