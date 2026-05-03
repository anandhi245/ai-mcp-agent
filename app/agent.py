from app.mcp_server import get_employee_details, create_ticket, list_tickets
import re
from app.mcp_server import get_system_status
from app.mcp_server import generate_employee_report
from app.mcp_server import get_employee_via_api
from app.mcp_server import add_employee
from app.mcp_server import get_employees_report
import google.genai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("GEMINI_API_KEY not found in environment")
    client = None
else:
    try:
        client = genai.Client(api_key=api_key)
        print("Gemini client initialized successfully")
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        client = None
def run_agent(user_input: str):
    if client is None:
        return {"error": "Gemini client not initialized"}
    
    prompt = f"""
Analyze the user message: "{user_input}"
Determine the appropriate action from these options:
- get_employee: Get details of an employee (needs emp_id)
- create_ticket: Create a support ticket (needs description)
- list_tickets: List all tickets
- add_employee: Add a new employee (needs emp_id, name, dept_id, salary)
- generate_report: Generate employee report
- get_system_status: Get system status
- get_employee_via_api: Get employee via API (needs emp_id)
- get_employees_report: Get a list of all employees

Extract relevant parameters from the message. For create_ticket, set description to the actual issue/request from the user's words, such as "jira access" for "raise ticket for jira access".
Return ONLY a valid JSON object in this format:
{{"action": "action_name", "params": {{"param1": "value1", ...}}}}
If no action matches, return {{"action": "unknown"}}
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-flash-latest',
            contents=prompt
        )
        result_text = response.candidates[0].content.parts[0].text.strip()
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result = json.loads(result_text)
        action = result.get("action")
        params = result.get("params", {})

        if action == "get_employee":
            emp_id = params.get("emp_id")
            if emp_id:
                return get_employee_details(int(emp_id))
        elif action == "create_ticket":
            description = params.get("description", user_input)
            return create_ticket(description)
        elif action == "list_tickets":
            return list_tickets()
        elif action == "add_employee":
            emp_id = params.get("emp_id")
            name = params.get("name")
            dept_id = params.get("dept_id")
            salary = params.get("salary")
            if emp_id and name and dept_id and salary:
                return add_employee(int(emp_id), name, int(dept_id), int(salary))
        elif action == "generate_report":
            return generate_employee_report()
        elif action == "get_system_status":
            return get_system_status()
        elif action == "get_employee_via_api":
            emp_id = params.get("emp_id")
            if emp_id:
                return get_employee_via_api(int(emp_id))
        elif action == "get_employees_report":
            return get_employees_report()
        else:
            return {"msg": "Not understood"}
    except Exception as e:
        return {"error": f"Failed to process: {str(e)}"}
