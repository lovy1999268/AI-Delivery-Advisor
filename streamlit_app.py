# streamlit_app.py
# Enterprise AI Recommendation Engine
# NOTE:
# This starter file is generated as a downloadable template.
# Replace/extend sections as needed to match your project.

import json
import streamlit as st
import roleselector

from openai_service import analyze_requirement, generate_recommendation
from database import (
    save_requirement,
    save_recommendation,
    get_workflow,
    get_automation,
    get_risk,
    get_validation
)

st.set_page_config(
    page_title="Enterprise AI Recommendation Engine",
    page_icon="🤖",
    layout="wide"
)
# ------------------------------------
# Role Selection
# ------------------------------------

# ------------------------------------
# Role Selection
# ------------------------------------

if "role" not in st.session_state:

    roleselector.show()

    st.stop()

# User has selected a role
role = st.session_state.role

# Sidebar
st.sidebar.title("👤 Current User")
st.sidebar.success(role)

st.sidebar.success(st.session_state.role)

st.title("🤖 Enterprise AI Recommendation Engine")
st.caption("Analyze requirements and generate AI-powered implementation recommendations.")

requirement = st.text_area(
    "Business Requirement",
    height=180,
    placeholder="Paste the business requirement here..."
)

if st.button("🚀 Analyze Requirement", use_container_width=True):

    if not requirement.strip():
        st.warning("Please enter a requirement.")
        st.stop()

    try:
        with st.spinner("Analyzing..."):

            result = analyze_requirement(requirement)
            data = json.loads(result)

            category = data.get("category","Unknown")
            priority = data.get("priority","Medium")

            title = requirement.split("\\n")[0][:100]

            requirement_id = save_requirement(
                title,
                requirement,
                category,
                priority,
                "AI Delivery Advisor"
            )

            workflows = get_workflow(category)
            automations = get_automation(category)
            risks = get_risk(category)
            validations = get_validation(category)

            report = generate_recommendation(
                requirement,
                workflows,
                automations,
                risks,
                validations
            )

            workflow_name = workflows[0][2] if workflows else "Unknown Workflow"

            save_recommendation(
                requirement_id,
                workflow_name,
                95
            )

        st.success("Analysis Completed")

        st.header("📄 Requirement")
        st.info(requirement)

        st.header("🤖 AI Classification")
        c1,c2,c3 = st.columns(3)
        c1.metric("Category",category)
        c2.metric("Priority",priority)
        c3.metric("Confidence","95%")

        st.header("🔄 Recommended Workflow")
        if workflows:
            for w in workflows:
                with st.container(border=True):
                    st.subheader(w[2])
                    if len(w)>3:
                        st.write(w[3])
        else:
            st.warning("No workflow found.")

        st.header("⚙ Recommended Automations")
        if automations:
            for a in automations:
                with st.expander(a[2]):
                    st.write("Trigger:",a[3])
                    st.write("Action:",a[4])

        st.header("✔ Validation Rules")
        if validations:
            for v in validations:
                st.success(v[2])

        st.header("⚠ Risks")
        if risks:
            for r in risks:
                with st.container(border=True):
                    st.error(r[2])
                    if len(r)>3:
                        st.write("Severity:",r[3])
                    if len(r)>4:
                        st.write("Mitigation:",r[4])

        st.header("🧠 Final Recommendation")
        st.markdown(report)

        with st.expander("Debug"):
            st.json(data)

    except Exception as ex:
        st.exception(ex)
st.sidebar.divider()

if st.sidebar.button("🚪 Change Role"):

    st.session_state.clear()

    st.rerun()