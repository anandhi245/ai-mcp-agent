from app.mcp_server import get_employee_details, create_ticket, list_tickets
import re
from app.mcp_server import get_system_status
from app.mcp_server import generate_employee_report
from app.mcp_server import get_employee_via_api
from app.mcp_server import add_employee
def extract_id(text):
    nums = re.findall(r'\d+', text)
    return int(nums[0]) if nums else None

def run_agent(user_input: str):
    text = user_input.lower()

    # 🔥 Multi-step workflow (more flexible)
    if "employee" in text and "ticket" in text:
        emp_id = extract_id(text)

        emp = get_employee_details(emp_id)
        ticket = create_ticket("Auto-created issue")

        return {
            "employee": emp,
            "ticket": ticket
        }

    # Add employee - format: "add employee id name dept_id salary"
    if "add employee" in text or "new employee" in text:
        nums = re.findall(r'\d+', text)
        if len(nums) >= 3:
            emp_id = int(nums[0])
            dept_id = int(nums[1])
            salary = int(nums[2])
            # Extract name - look for text between the first number and next number
            name_match = re.search(r'add employee\s+\d+\s+(\w+)', user_input.lower())
            name = name_match.group(1) if name_match else "Unknown"
            return add_employee(emp_id, name, dept_id, salary)
        return {"error": "Use format: add employee <id> <name> <dept_id> <salary>"}

    # Employee
    if "employee" in text:
        emp_id = extract_id(text)
        return get_employee_details(emp_id)

    # Create ticket
    if "ticket" in text and any(word in text for word in ["create", "raise", "add"]):
        return create_ticket(user_input)

    # List tickets
    if "ticket" in text and any(word in text for word in ["list", "show", "all"]):
        return list_tickets()

    # Report
    if "report" in text:
        return generate_employee_report()

    # API
    if "api" in text and "employee" in text:
        emp_id = extract_id(text)
        return get_employee_via_api(emp_id)

    # System
    if "system" in text:
        return get_system_status()

    return {"msg": "Not understood"}