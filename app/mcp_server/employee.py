from app.database import get_connection
from app.api_simulation import get_employee_api

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

def get_employees_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()

    # Format the data as a list of dictionaries
    employees = []
    for row in data:
        employees.append({
            "id": row[0],
            "name": row[1],
            "department_id": row[2],
            "salary": row[3]
        })

    return employees