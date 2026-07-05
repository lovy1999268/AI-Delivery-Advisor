import pandas as pd
import os
import sys

# Load .env file if available (local development only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Determine platform
IS_WINDOWS = sys.platform.startswith('win')


# ==================================================
# SQL SERVER CONNECTION
# ==================================================

def get_connection():
    """
    Connect to SQL Server with proper handling for:
    - Local Windows: pyodbc + Windows Authentication
    - Streamlit Cloud: pymssql + SQL Authentication
    
    Reads config from:
    1. Streamlit secrets (st.secrets) - for cloud
    2. Environment variables (.env) - for local
    """
    
    # Get database credentials
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME", "AI_Delivery_Advisor")
    username = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()
    
    # Try Streamlit secrets (overrides .env)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and st.secrets:
            server = st.secrets.get("DB_SERVER", server)
            database = st.secrets.get("DB_NAME", database)
            username = st.secrets.get("DB_USER", username)
            password = st.secrets.get("DB_PASSWORD", password)
    except (ImportError, Exception):
        pass
    
    # Validate server is set
    if not server:
        raise ValueError(
            "DB_SERVER not configured. "
            "Set DB_SERVER in .env (local) or Streamlit Secrets (cloud)"
        )
    
    # ===== LOCAL DEVELOPMENT (Windows + pyodbc) =====
    if IS_WINDOWS and not (username and password):
        try:
            import pyodbc
        except ImportError:
            raise ImportError("pyodbc not installed. Run: pip install pyodbc")
        
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            raise RuntimeError(
                f"Local connection failed: {str(e)}\n"
                f"Server: {server}\n"
                f"Database: {database}\n"
                f"Make sure SQL Server is running: Services > SQL Server (MSSQLSERVER)"
            ) from e
    
    # ===== CLOUD DEPLOYMENT (any OS + pymssql with SQL Auth) =====
    elif username and password:
        try:
            import pymssql
        except ImportError:
            raise ImportError("pymssql not installed. Run: pip install pymssql")
        
        try:
            conn = pymssql.connect(
                server=server,
                user=username,
                password=password,
                database=database,
                tds_version="7.2",
                timeout=10
            )
            return conn
        except Exception as e:
            raise RuntimeError(
                f"Cloud connection failed: {str(e)}\n"
                f"Server: {server}\n"
                f"User: {username}\n"
                f"Database: {database}\n"
                f"Check DB_SERVER, DB_USER, DB_PASSWORD in Streamlit Secrets"
            ) from e
    
    # ===== ERROR: No credentials provided =====
    else:
        raise ValueError(
            "Database credentials not configured!\n\n"
            "For LOCAL development: "
            "Set DB_SERVER in .env (leave DB_USER and DB_PASSWORD empty)\n\n"
            "For STREAMLIT CLOUD: "
            "Set DB_SERVER, DB_USER, and DB_PASSWORD in Streamlit Secrets"
        )


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