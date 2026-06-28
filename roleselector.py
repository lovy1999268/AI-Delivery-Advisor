import streamlit as st

def show():

    st.markdown(
        """
        <h1 style='text-align:center;color:#2563EB;'>
        🤖 Enterprise AI Recommendation Engine
        </h1>

        <h4 style='text-align:center;color:gray;'>
        AI Powered Requirement Analysis Platform
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.subheader("👤 Select Your Role")

    role = st.selectbox(
        "Role",
        [
            "Business Analyst",
            "Release Manager",
            "Admin"
        ]
    )

    st.write("")

    if st.button("🚀 Enter Application", use_container_width=True):

        st.session_state.role = role

        st.rerun()