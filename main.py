from enum import Enum
from fastapi import FastAPI
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