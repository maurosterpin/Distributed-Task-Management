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

@app.get("/tasks/")
def get_task_by_params(
    name: str | None = None, 
    description: str | None = None, 
    assigne: str | None = None,
    owner: str | None = None, 
    status: Status | None = None, 
) -> dict[str, dict[str, str | Status | None]]:
    def check_task(task: Task) -> bool:
        return all(
            (
                name is None or task.name == name,
                description is None or task.description == description,
                assigne is None or task.assigne == assigne,
                owner is None or task.owner == owner,
                status is None or task.status is status
            )
        )
    res = [task for task in tasks.values() if check_task(task)]
    return {
        "query": {"name": name, "description": description, "assigne": assigne, "owner": owner, "status": status},
        "res": res
    }