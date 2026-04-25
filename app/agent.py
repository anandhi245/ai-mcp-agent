from app.mcp_server import get_employee_details, create_ticket, list_tickets
import re
from app.mcp_server import get_system_status
from app.mcp_server import generate_employee_report
from app.mcp_server import get_employee_via_api
def extract_id(text):
    nums = re.findall(r'\d+', text)
    return int(nums[0]) if nums else None

def run_agent(user_input: str):
    text = user_input.lower()

    # Employee
    if "employee" in text:
        emp_id = extract_id(text)
        return get_employee_details(emp_id)
# Create ticket (improved)
    if "ticket" in text and any(word in text for word in ["create", "raise", "add"]):
        return create_ticket(user_input)
    
    if "ticket" in text and any(word in text for word in ["list", "show", "all"]):
        return list_tickets()
 
    if "report" in text:
        return generate_employee_report()
    # Multi-step workflow
    if "create ticket and get employee" in text:
        emp_id = extract_id(text)
        emp = get_employee_details(emp_id)
        ticket = create_ticket("Auto-created issue")

        return {
        "employee": emp,
        "ticket": ticket
    }
    if "api employee" in text:
        emp_id = extract_id(text)
        return get_employee_via_api(emp_id)
    if "system" in text:
        return get_system_status()
    return {"msg": "Not understood"}
    