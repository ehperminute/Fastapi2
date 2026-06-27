import sqlite3

DATABASE_NAME = "sales.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)
