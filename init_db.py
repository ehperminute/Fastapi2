import pandas as pd
import sqlite3

conn = sqlite3.connect("tasks.db")
# insert all rows from csv
cursor = conn.cursor()
cursor.execute("drop table if exists tasks")
cursor.execute(""" CREATE TABLE IF NOT EXISTS tasks
(  
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  completed INTEGER NOT NULL,
  list_id INTEGER NOT NULL
)""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS task_lists
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT
)""")
conn.commit()
conn.close()
