from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
from .db import task_table

class Task(BaseModel):
    id: str
    title: str
    desc: str
    owner: str
    assignee: str
    status: str

def get_task(task_id: str) -> Task:
    try:
        response = task_table.get_item(Key={'id': task_id})
        item = response.get('Item', None)
        if item is None:
            raise Exception(f"Task with id '{task_id}' does not exist.")
        return Task(**item)
    except Exception as e:
        raise Exception(f"Error retrieving task: {str(e)}")

def create_task(task: Task) -> dict:
    try:
        task_table.put_item(Item=task.dict())
        return {"message": "Task upserted successfully"}
    except Exception as e:
        raise Exception(f"Error creating task: {str(e)}")
