import sqlite3

DB_PATH = "data/company.db"

def get_connection():
    return sqlite3.connect(DB_PATH)