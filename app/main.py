from fastapi import FastAPI, HTTPException
from .task_service import Task, get_task, create_task
from .user_service import User, get_user, create_user

app = FastAPI()

@app.get("/tasks/{task_id}")
async def read_task(task_id: str):
    try:
        task: Task = get_task(task_id)
        owner: User = get_user(task["owner"])
        assignee: User = get_user(task["assignee"])
        if task:
            task["owner"] = owner["name"]
            task["assignee"] = assignee["name"]
            return task
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def upsert_task(task: Task):
    try:
        get_user(task.owner)
        get_user(task.assignee)
        result = create_task(task)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/users")
async def upsert_user(user: User):
    try:
        result = create_user(user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
