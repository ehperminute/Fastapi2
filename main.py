from fastapi import FastAPI, HTTPException 
from models import TaskList, Task
from database import get_connection


app = FastAPI()

@app.get("/lists")
def get_lists():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT DISTINCT name FROM task_lists;")
  return {"task_lists": {"id": id, "name": name for id, name in cursor.fetchall()}}

@app.post("/lists")
def post_lists(list: TaskList):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("? IN (SELECT DISTINCT name FROM task_lists;)", list.name)
  res = cursor.fetchone()[0]
  if res == "1":
    conn.close()
    raise HTTPException(status_code=422, detail=f"list {list.name} already exists")
  cursor.execute("INSERT INTO task_lists(name) VALUES(?)", list.name)
  conn.commit()
  conn.close()
  return f"task_list {list.name} has been created"
