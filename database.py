import pandas as pd
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Determine which driver to use based on platform
# Use pymssql on Linux/Cloud (no ODBC drivers), pyodbc on Windows
IS_WINDOWS = sys.platform.startswith('win')

if IS_WINDOWS:
    try:
        import pyodbc
        USING_PYODBC = True
    except ImportError:
        USING_PYODBC = False
        import pymssql
else:
    # Force pymssql on Linux/Cloud environments
    USING_PYODBC = False
    import pymssql

# ==================================================
# HELPER FUNCTIONS FOR CONFIGURATION
# ==================================================

def get_config(key, default=None):
    """
    Get configuration from multiple sources (in order of priority):
    1. Streamlit secrets (st.secrets) - for cloud deployments
    2. Environment variables (.env) - for local development
    3. Default value
    """
    # Try Streamlit secrets first (available on Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, Exception):
        pass
    
    # Fall back to environment variables
    env_value = os.getenv(key)
    if env_value is not None:
        return env_value
    
    return default


# ==================================================
# SQL SERVER CONNECTION
# ==================================================

def get_connection():
    """
    Connect to SQL Server using:
    - pyodbc on Windows (with ODBC drivers)
    - pymssql on Linux/Cloud (pure Python driver)
    
    Configuration can come from:
    - Streamlit Cloud secrets
    - Local .env file
    """
    server = get_config("DB_SERVER", "localhost")
    database = get_config("DB_NAME", "AI_Delivery_Advisor")
    username = get_config("DB_USER")
    password = get_config("DB_PASSWORD")
    
    # For SQL Server Authentication (cloud/production with username/password)
    if username and password:
        if USING_PYODBC:
            try:
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                    f"TrustServerCertificate=yes;"
                )
                return pyodbc.connect(connection_string)
            except Exception as e:
                raise RuntimeError(
                    f"pyodbc connection failed: {str(e)}. "
                    "This usually means ODBC drivers are not installed. "
                    "On Windows, install 'ODBC Driver 17 for SQL Server'. "
                    "On Linux/Cloud, ensure DB_SERVER uses format: server.database.windows.net"
                ) from e
        else:
            # Use pymssql for Linux/Cloud environments
            try:
                return pymssql.connect(
                    server=server,
                    user=username,
                    password=password,
                    database=database,
                    tds_version="7.2",
                    timeout=10
                )
            except Exception as e:
                raise RuntimeError(
                    f"pymssql connection failed: {str(e)}. "
                    "Check that DB_SERVER, DB_USER, and DB_PASSWORD are correctly configured in Streamlit Secrets. "
                    f"Verify server format: 'server.database.windows.net' for Azure SQL or 'hostname:port' for on-premises"
                ) from e
    
    # For Windows Authentication (local development only)
    else:
        if not USING_PYODBC:
            raise RuntimeError(
                "Windows Authentication requires pyodbc on Windows. "
                "For cloud deployments (Linux/Streamlit Cloud), you MUST provide DB_USER and DB_PASSWORD in Streamlit Secrets. "
                "Steps: 1) Go to your Streamlit Cloud app settings. 2) Click 'Secrets'. 3) Add DB_USER, DB_PASSWORD, DB_SERVER."
            )
        
        try:
            connection_string = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
            return pyodbc.connect(connection_string)
        except Exception as e:
            raise RuntimeError(f"pyodbc connection with Windows auth failed: {str(e)}") from e


# ==================================================
# SAVE REQUIREMENT
# ==================================================

def save_requirement(title, description, category, priority, project_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO RequirementLibrary
        (
            RequirementTitle,
            RequirementDescription,
            Category,
            Priority,
            ProjectType
        )
        OUTPUT INSERTED.RequirementID
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        title,
        description,
        category,
        priority,
        project_type
    ))

    requirement_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return requirement_id


# ==================================================
# WORKFLOW LIBRARY
# ==================================================

def get_workflow(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM WorkflowLibrary
        WHERE Category = ?
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# AUTOMATION LIBRARY
# ==================================================

def get_automation(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM AutomationLibrary
        WHERE Category = ?
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# RISK LIBRARY
# ==================================================

def get_risk(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM RiskLibrary
        WHERE Category = ?
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# VALIDATION LIBRARY
# ==================================================

def get_validation(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM ValidationLibrary
        WHERE Category = ?
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# SAVE RECOMMENDATION
# ==================================================

def save_recommendation(requirement_id, workflow, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO RecommendationHistory
        (
            RequirementID,
            RecommendedWorkflow,
            RecommendationDate,
            ConfidenceScore,
            Status
        )
        VALUES (?, ?, GETDATE(), ?, ?)
    """,
    (
        requirement_id,
        workflow,
        confidence,
        "Generated"
    ))

    conn.commit()
    conn.close()


# ==================================================
# RECOMMENDATION HISTORY
# ==================================================

def get_recommendation_history():

    conn = get_connection()

    query = """
        SELECT
            RecommendationID,
            RequirementID,
            RecommendedWorkflow,
            RecommendationDate,
            ConfidenceScore,
            Status
        FROM RecommendationHistory
        ORDER BY RecommendationDate DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==================================================
# REQUIREMENT HISTORY
# ==================================================

def get_requirement_history():

    conn = get_connection()

    query = """
        SELECT *
        FROM RequirementLibrary
        ORDER BY CreatedDate DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==================================================
# DASHBOARD DATA
# ==================================================


def get_all_workflows():

    conn = get_connection()

    query = """
    SELECT
        WorkflowID,
        Category,
        WorkflowName,
        WorkflowDescription,
        ProjectsUsing,
        SuccessRate,
        EstimatedHours
    FROM WorkflowLibrary
    ORDER BY WorkflowName
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def get_dashboard_data():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Requirements
    cursor.execute("""
        SELECT COUNT(*)
        FROM RequirementLibrary
    """)
    total_requirements = cursor.fetchone()[0]

    # Total Recommendations
    cursor.execute("""
        SELECT COUNT(*)
        FROM RecommendationHistory
    """)
    total_recommendations = cursor.fetchone()[0]

    # Average Confidence
    cursor.execute("""
        SELECT AVG(ConfidenceScore)
        FROM RecommendationHistory
    """)
    avg_confidence = cursor.fetchone()[0]

    if avg_confidence is None:
        avg_confidence = 0

    # Generated Reports
    cursor.execute("""
        SELECT COUNT(*)
        FROM RecommendationHistory
        WHERE Status='Generated'
    """)
    generated_reports = cursor.fetchone()[0]

    conn.close()

    return (
        total_requirements,
        total_recommendations,
        avg_confidence,
        generated_reports
    )

def update_workflow(
    workflow_id,
    workflow_name,
    category,
    description,
    projects,
    success_rate,
    hours
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE WorkflowLibrary
    SET
        WorkflowName=?,
        Category=?,
        WorkflowDescription=?,
        ProjectsUsing=?,
        SuccessRate=?,
        EstimatedHours=?
    WHERE WorkflowID=?
""",
(
    workflow_name,
    category,
    description,
    int(projects),
    float(success_rate),
    float(hours),
    int(workflow_id)
))
    conn.commit()
    conn.close()

def delete_workflow(workflow_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM WorkflowLibrary
        WHERE WorkflowID = ?
    """,
    (
        int(workflow_id),
    ))

    conn.commit()
    conn.close()    