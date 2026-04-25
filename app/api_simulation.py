from app.database import get_connection

def get_employee_api(emp_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "id": result[0],
            "name": result[1],
            "department": result[2],
            "salary": result[3]
        }
    return {"error": "Not found"}