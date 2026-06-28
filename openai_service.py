from ollama import chat

def analyze_requirement(requirement):

    prompt = f"""
You are an AI Requirement Analyzer.

Return ONLY valid JSON.

Requirement:
{requirement}

Format:

{{
  "category":"",
  "priority":"",
  "workflow":"",
  "automation":"",
  "risk":""
}}

Only output JSON.
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def generate_recommendation(requirement, workflows, automations, risks, validations):

    prompt = f"""
You are a Senior Enterprise Solution Architect.

Requirement

{requirement}

Workflow Library

{workflows}

Automation Library

{automations}

Risk Library

{risks}

Validation Library

{validations}

Generate a professional report.

Return:

1. Requirement Summary

2. Business Impact

3. Recommended Workflow

4. Recommended Automations

5. Validation Rules

6. Risks

7. Estimated Time Saved

8. Confidence Score

9. Implementation Steps
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response["message"]["content"]