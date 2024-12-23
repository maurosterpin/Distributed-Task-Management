from fastapi import FastAPI, HTTPException
from .task_service import Task, get_task, create_task

app = FastAPI()

@app.get("/tasks/{task_id}")
async def read_task(task_id: str):
    try:
        task = get_task(task_id)
        if task:
            return task
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def upsert_task(task: Task):
    try:
        result = create_task(task)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
