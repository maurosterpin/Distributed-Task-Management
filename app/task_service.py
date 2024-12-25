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

def get_task(task_id: str):
    try:
        response = task_table.get_item(Key={'id': task_id})
        return response.get('Item', None)
    except Exception as e:
        raise Exception(f"Error retrieving task: {str(e)}")

def create_task(task: Task):
    try:
        task_table.put_item(Item=task.dict())
        return {"message": "Task created successfully"}
    except Exception as e:
        raise Exception(f"Error creating task: {str(e)}")
