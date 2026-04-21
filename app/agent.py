from app.mcp_server import get_employee_details
import re

def extract_id(text):
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None

def run_agent(user_input: str):
    user_input = user_input.lower()

    if "employee" in user_input:
        emp_id = extract_id(user_input)
        if emp_id:
            return get_employee_details(emp_id)
        else:
            return {"error": "No employee ID found"}

    return {"message": "Sorry, I don't understand"}