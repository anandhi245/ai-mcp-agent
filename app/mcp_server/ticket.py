from app.database import get_connection

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

    return {"ticket_id": ticket_id, "issue": issue, "status": "Open"}

def list_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    data = cursor.fetchall()
    conn.close()

    return data
