import json

from openai_service import analyze_requirement, generate_recommendation
from database import (
    get_workflow,
    get_automation,
    get_risk,
    get_validation
)

requirement = """
Manager approval is required before Production deployment.

If approval is not received within 24 hours,
notify the Release Manager.

Only Release Managers can approve.
"""

# Step 1: AI classifies the requirement
result = analyze_requirement(requirement)

print("AI Classification:")
print(result)

# Step 2: Convert JSON to Python object
data = json.loads(result)

category = data["category"]

print("\nCategory:", category)

# Step 3: Query SQL
workflows = get_workflow(category)
automations = get_automation(category)
risks = get_risk(category)
validations = get_validation(category)

# Step 4: Generate final recommendation
final_report = generate_recommendation(
    requirement,
    workflows,
    automations,
    risks,
    validations
)

print("\n===================================")
print(" AI FINAL RECOMMENDATION ")
print("===================================\n")

print(final_report)