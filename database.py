import pyodbc
import pandas as pd


# ==================================================
# SQL SERVER CONNECTION
# ==================================================

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=AI_Delivery_Advisor;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
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