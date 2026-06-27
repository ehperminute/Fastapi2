from pydantic import BaseModel, Field

class TaskList(BaseModel):
  name: str = Field(min_length=1)

class Task(BaseModel):
  title: str = Field(min_length=1)
  list_id: int = Field(ge=1)
