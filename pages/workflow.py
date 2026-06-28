import streamlit as st

# -----------------------------
# Check Role
# -----------------------------

if "role" not in st.session_state:
    st.error("Please select a role.")
    st.stop()

# -----------------------------
# Allow Only Admin
# -----------------------------

if st.session_state.role != "Admin":
    st.error("🚫 Access Denied")
    st.info("Only Admin can access Workflow Library.")
    st.stop()

# -----------------------------
# Page Content
# -----------------------------

st.title("⚙ Workflow Library")

st.success("Welcome Admin!")
from database import (
    get_all_workflows,
    update_workflow,
    delete_workflow
)

df = get_all_workflows()
# ------------------------------------------
# KPI Cards
# ------------------------------------------

total_workflows = len(df)

avg_success = df["SuccessRate"].mean()

avg_hours = df["EstimatedHours"].mean()

total_projects = df["ProjectsUsing"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📄 Total Workflows",
        total_workflows
    )

with col2:
    st.metric(
        "📈 Avg Success Rate",
        f"{avg_success:.1f}%"
    )

with col3:
    st.metric(
        "⏱ Avg Hours",
        f"{avg_hours:.1f}"
    )

with col4:
    st.metric(
        "🏢 Projects Using",
        total_projects
    )

st.divider()

st.subheader("📚 Available Workflows")

search = st.text_input("🔍 Search Workflow")

category = st.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

filtered_df = df.copy()

# Search
if search:
    filtered_df = filtered_df[
        filtered_df["WorkflowName"].str.contains(search, case=False)
    ]

# Category Filter
if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

st.write("")

# Display each workflow as a card
for _, row in filtered_df.iterrows():

    with st.container(border=True):

        col1, col2 = st.columns([3,1])

        with col1:

            st.subheader(f"⚙ {row['WorkflowName']}")

            st.write(f"**Category:** {row['Category']}")

            st.write(row["WorkflowDescription"])

        with col2:

            st.metric(
                "Projects",
                row["ProjectsUsing"]
            )

            st.metric(
                "Hours",
                row["EstimatedHours"]
            )

        st.progress(row["SuccessRate"] / 100)

        st.caption(f"Success Rate: {row['SuccessRate']}%")

        st.divider()

        # ---------------------------------
        # ACTION BUTTONS
        # ---------------------------------

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button(
                "👁 View",
                key=f"view_{row['WorkflowID']}"
            ):
                st.session_state.selected_workflow = row["WorkflowID"]

        with b2:
           if st.button(
              "✏ Edit",
              key=f"edit_{row['WorkflowID']}"
    ):
              st.session_state.edit_workflow = row["WorkflowID"]
        with b3:
            if st.button(
            "🗑 Delete",
              key=f"delete_{row['WorkflowID']}"
    ):
              st.success("Delete button clicked")
              st.session_state.delete_workflow = row["WorkflowID"]
              # -----------------------------------------
# EDIT WORKFLOW
# -----------------------------------------

if "edit_workflow" in st.session_state:

    edit_df = df[
        df["WorkflowID"] == st.session_state.edit_workflow
    ]

    if not edit_df.empty:

        workflow = edit_df.iloc[0]

        st.divider()
        st.subheader("✏ Edit Workflow")

        workflow_name = st.text_input(
            "Workflow Name",
            value=workflow["WorkflowName"]
        )

        category = st.text_input(
            "Category",
            value=workflow["Category"]
        )

        description = st.text_area(
            "Description",
            value=workflow["WorkflowDescription"]
        )

        projects = st.number_input(
            "Projects Using",
            value=int(workflow["ProjectsUsing"])
        )

        success_rate = st.number_input(
            "Success Rate",
            value=float(workflow["SuccessRate"])
        )

        estimated_hours = st.number_input(
            "Estimated Hours",
            value=float(workflow["EstimatedHours"])
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Save Changes"):

                update_workflow(
                    workflow["WorkflowID"],
                    workflow_name,
                    category,
                    description,
                    projects,
                    success_rate,
                    estimated_hours
                )

                st.success("Workflow Updated Successfully!")

                del st.session_state.edit_workflow

                st.rerun()

        with col2:
            if st.button("❌ Cancel"):

                del st.session_state.edit_workflow

                st.rerun()

        

# -----------------------------------------
# VIEW DETAILS
# -----------------------------------------

if "selected_workflow" in st.session_state:

    workflow = filtered_df[
        filtered_df["WorkflowID"] ==
        st.session_state.selected_workflow
    ]

    if not workflow.empty:

        st.divider()

        st.subheader("📄 Workflow Details")

        st.json(workflow.iloc[0].to_dict())
        # -----------------------------------------
# DELETE WORKFLOW
# -----------------------------------------

if "delete_workflow" in st.session_state:

    workflow = df[
        df["WorkflowID"] == st.session_state.delete_workflow
    ]

    if not workflow.empty:

        workflow = workflow.iloc[0]

        st.divider()

        st.error("⚠ Delete Workflow")

        st.write(
            f"Are you sure you want to delete **{workflow['WorkflowName']}**?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✅ Yes Delete"):

                delete_workflow(workflow["WorkflowID"])

                del st.session_state.delete_workflow

                st.session_state.delete_workflow = row["WorkflowID"]



                st.rerun()

        with col2:

            if st.button("❌ Cancel"):

                del st.session_state.delete_workflow

                st.rerun()