import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/company.db")
cursor = conn.cursor()

# Create employee table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

# Insert sample data
employees = [
    (1001, "Rahul", "IT", 70000),
    (1002, "Priya", "HR", 65000),
    (1003, "Amit", "Finance", 72000),
]

cursor.executemany("INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)", employees)

conn.commit()
conn.close()

print("Database initialized!")