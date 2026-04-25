import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/company.db")
cursor = conn.cursor()

# Drop old tables (for clean setup)
cursor.execute("DROP TABLE IF EXISTS tickets")
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS departments")

# -----------------------------
# Departments Table
# -----------------------------
cursor.execute("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
)
""")

# -----------------------------
# Employees Table
# -----------------------------
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department_id INTEGER,
    salary INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")

# -----------------------------
# Tickets Table
# -----------------------------
cursor.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    status TEXT,
    employee_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
""")

# -----------------------------
# Insert Departments
# -----------------------------
departments = [
    (1, "IT"),
    (2, "HR"),
    (3, "Finance"),
    (4, "Marketing")
]

cursor.executemany("INSERT INTO departments VALUES (?, ?)", departments)

# -----------------------------
# Insert 20 Employees
# -----------------------------
employees = [
    (1001, "Rahul", 1, 70000),
    (1002, "Priya", 2, 65000),
    (1003, "Amit", 3, 72000),
    (1004, "Sneha", 1, 68000),
    (1005, "Kiran", 4, 60000),
    (1006, "Arjun", 1, 75000),
    (1007, "Neha", 2, 64000),
    (1008, "Ravi", 3, 71000),
    (1009, "Pooja", 4, 62000),
    (1010, "Manish", 1, 73000),
    (1011, "Divya", 2, 66000),
    (1012, "Suresh", 3, 74000),
    (1013, "Anita", 4, 61000),
    (1014, "Vikram", 1, 76000),
    (1015, "Meena", 2, 65000),
    (1016, "Rohit", 3, 72000),
    (1017, "Swathi", 4, 63000),
    (1018, "Ajay", 1, 77000),
    (1019, "Lakshmi", 2, 66000),
    (1020, "Karthik", 3, 75000)
]

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees)

# -----------------------------
# Insert Sample Tickets
# -----------------------------
tickets = [
    ("Login issue", "Open", 1001),
    ("Password reset", "Closed", 1002),
    ("System crash", "Open", 1003),
    ("Email issue", "Open", 1004),
    ("Network slow", "Closed", 1005),
]

cursor.executemany("INSERT INTO tickets(issue, status, employee_id) VALUES (?, ?, ?)", tickets)

conn.commit()
conn.close()

print("Database initialized with normalized schema and 20+ records!")