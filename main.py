from fastapi import FastAPI, HTTPException 
from models import 
from database import get_connection


app = FastAPI()

@app.get("/lists")
def get_lists():
  conn = get_connection
