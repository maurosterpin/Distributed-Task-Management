from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    DONE = "done"

class Task(BaseModel):
    name: str
    description: str
    assigne: str
    owner: str
    status: Status

tasks = {
    0: Task(name="Make app", description="Make task management app", assigne="mauro", owner="mauro", status=Status.TODO),
    1: Task(name="Eat", description="Make breakfast", assigne="mauro", owner="mauro", status=Status.TODO)
}

@app.get("/")
def index() -> dict[str, dict[int, Task]]:
    return {"tasks": tasks}

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist")
    return tasks[task_id]