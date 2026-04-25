from app.database import get_connection

from app.api_simulation import get_employee_api
import random

def get_system_status():
    return {
        "cpu_usage": f"{random.randint(20,80)}%",
        "memory_usage": f"{random.randint(30,70)}%",
        "status": "Running"
    }
def get_employee_via_api(emp_id: int):
    return get_employee_api(emp_id)

def get_employee_details(emp_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT e.id, e.name, d.name, e.salary
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    WHERE e.id=?
    """, (emp_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "id": result[0],
            "name": result[1],
            "department": result[2],
            "salary": result[3]
        }

    return {"error": "Employee not found"}
   

# NEW
def create_ticket(issue: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tickets(issue, status) VALUES (?, ?)",
        (issue, "Open")
    )
    conn.commit()

    ticket_id = cursor.lastrowid
    conn.close()

    return {"ticket_id": ticket_id, "status": "Open"}


def list_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    data = cursor.fetchall()
    conn.close()

    return data
def generate_employee_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT d.name, COUNT(e.id) 
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        GROUP BY e.department_id
    """)
    dept_data = cursor.fetchall()

    conn.close()

    return {
        "total_employees": total,
        "department_distribution": [{"department": row[0], "count": row[1]} for row in dept_data]
    }


def add_employee(emp_id: int, name: str, department_id: int, salary: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(id, name, department_id, salary) VALUES (?, ?, ?, ?)",
        (emp_id, name, department_id, salary)
    )
    conn.commit()
    conn.close()

    # Return the added employee details
    return get_employee_details(emp_id)