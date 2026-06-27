from fastapi import FastAPI, HTTPException 
from models import TaskList, Task
from database import get_connection


app = FastAPI()

@app.get("/lists")
def get_lists():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT id, name FROM task_lists;")
  rows = cursor.fetchall()
  conn.close()
  return {"task_lists": [{"id": id, "name": name} for id, name in rows]}

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
    SELECT DISTINCT t.id, t.title, tl.name, t.completed 
    FROM task_lists tl
      JOIN tasks t ON t.list_id = tl.id
    ORDER BY tl.id, t.id;
    """)
  rows = cursor.fetchall()
  conn.close()
  return {"tasks": [{"id": id, "title": title, "list": list, "completed": completed}
          for id, title, list, completed in rows]}

@app.post("/tasks")
def post_task(task: Task):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT title FROM tasks WHERE title = ?", (task.title,))
  exists = cursor.fetchone()
  if exists:
    conn.close()
    raise HTTPException(status_code=422, detail=f"task {task.title} already exists")

  cursor.execute("SELECT id FROM task_lists WHERE id = ?", (task.list_id,))

  exists = cursor.fetchone()
  if not exists:
    conn.close()
    raise HTTPException(status_code=404, detail=f"list with id {task.list_id} doesn't exist")
  cursor.execute("INSERT INTO tasks(title, list_id, completed) VALUES(?, ?, 0)", (task.title, task.list_id))
  conn.commit()
  conn.close()
  return f"task {task.title} has been created in list_id {task.list_id}"


@app.put("/tasks/{task_id}")
def put_task(task_id: int):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT title FROM tasks WHERE id = ?", (task_id,))
  exists = cursor.fetchone()
  if not exists:
    conn.close()
    raise HTTPException(status_code=404, detail=f"task with id={task_id} doesn't exist")
  cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
  conn.commit()
  conn.close()
  return f"task {task_id} has been marked as completed"

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT title FROM tasks WHERE id = ?", (task_id,))
  exists = cursor.fetchone()
  if not exists:
    conn.close()
    raise HTTPException(status_code=404, detail=f"task with id={task_id} doesn't exist")
  cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
  conn.commit()
  conn.close()
  return f"task with id={task_id} has been deleted"

@app.get("/lists/{list_id}/tasks")
def get_list_tasks(list_id: int):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM task_lists WHERE id = ?", (list_id,))
  exists = cursor.fetchone()
  if not exists:
    conn.close()
    raise HTTPException(status_code=404, detail=f"list with id={list_id} doesn't exist")
  cursor.execute("""
    SELECT DISTINCT t.id, t.title, tl.name, t.completed 
    FROM task_lists tl
      JOIN tasks t ON t.list_id = tl.id
    WHERE tl.id = ?
    ORDER BY tl.id, t.id;
    """, (list_id,))
  rows = cursor.fetchall()
  conn.close()
  return {f"tasks in list (id={list_id})": [{"id": id, "title": title, "list": list, "completed": completed} 
                                            for id, title, list, completed in rows]}
