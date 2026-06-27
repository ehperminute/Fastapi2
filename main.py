from fastapi import FastAPI, HTTPException 
from models import TaskList, Task
from database import get_connection


app = FastAPI()

@app.get("/lists")
def get_lists():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT id, name FROM task_lists;")
  return {"task_lists": [{"id": id, "name": name} for id, name in cursor.fetchall()]}

@app.post("/lists")
def post_lists(list: TaskList):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM task_lists WHERE name = ?", (list.name,))
  exists = cursor.fetchone()
  if exists:
    print(exists)
    conn.close()
    raise HTTPException(status_code=422, detail=f"list {list.name} already exists")
  cursor.execute("INSERT INTO task_lists(name) VALUES(?)", (list.name,))
  conn.commit()
  conn.close()
  return {"message": f"task_list {list.name} has been created"}

@app.get("/tasks")
def get_tasks():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("""
    SELECT DISTINCT t.id, tl.name, t.title, t.completed 
    FROM task_lists tl
      JOIN tasks t ON t.list_id = tl.id
    ORDER BY tl.id, t.id;
    """)
  return {"tasks": [{"id": id, "name": name, "list": list, "completed": completed}
          for id, name, list, completed in cursor.fetchall()]}

@app.post("/tasks")
def post_lists(task: Task):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT DISTINCT title FROM tasks WHERE title = ?", (task.title,))
  exists = cursor.fetchone()
  if exists:
    conn.close()
    raise HTTPException(status_code=422, detail=f"task {task.title} already exists")

  cursor.execute("SELECT ? IN (SELECT DISTINCT list_id FROM tasks)", (task.list_id,))
  res = cursor.fetchone()[0]
  if res == "0":
    conn.close()
    raise HTTPException(status_code=404, detail=f"list with id {task.list_id} doesn't exist")
  cursor.execute("INSERT INTO task_lists(name) VALUES(?)", (task.title,))
  conn.commit()
  conn.close()
  return f"task {task.title} has been created in list_id {task.list_id}"


@app.put("/tasks/{id}")
def post_lists(task_id: int):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT ? IN (SELECT DISTINCT title FROM tasks)", (task_id,))
  res = cursor.fetchone()[0]
  if res == "0":
    conn.close()
    raise HTTPException(status_code=404, detail=f"task with id={task_id} doesn't exist")
  cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", task.id)
  conn.commit()
  conn.close()
  return f"task {task.title} has been marked as completed"

@app.delete("/tasks/{id}")
def post_lists(task_id: int):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT ? IN (SELECT DISTINCT title FROM tasks)", (task.title,))
  res = cursor.fetchone()[0]
  if res == "0":
    conn.close()
    raise HTTPException(status_code=404, detail=f"task with id={task_id} doesn't exist")
  cursor.execute("DELETE FROM tasks WHERE id = ?", task.id)
  conn.commit()
  conn.close()
  return f"task with id={task_id} has been marked deleted"

@app.get("/lists/{list_id}/tasks")
def get_list_tasks(list_id):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT ? IN (SELECT DISTINCT name FROM task_lists)", (list.name,))
  res = cursor.fetchone()[0]
  if res == "0":
    conn.close()
    raise HTTPException(status_code=404, detail=f"list {list.name} doesn't exist")
  cursor.execute("""
    SELECT DISTINCT t.id, t.title, t.completed 
    FROM task_lists tl
      JOIN tasks t ON t.list_id = tl.list_id
    ORDER BY tl.id, t.id;
    """)
  return {f"tasks in list (id={list_id})": [{"id": id, "name": name, "list": list, "completed": completed} 
                                            for id, name, list, completed in cursor.fetchall()]}
