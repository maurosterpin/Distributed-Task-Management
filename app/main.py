from fastapi import FastAPI, Depends
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import boto3

app = FastAPI()

dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:4566", region_name='us-east-1',
                           aws_access_key_id="access_key_id", 
                           aws_secret_access_key="secret")

def create_table(table_name):
    print(f"Creating table '{table_name}'...")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    print("Table created successfully!")

create_table('your_table_name')
table = dynamodb.Table('your_table_name')

class Task(BaseModel):
    id: str
    title: str
    desc: str
    owner: str
    assignee: str
    status: str

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    try:
        response = table.get_item(Key={'id': task_id})
        item = response['Item']
        return item
    except Exception as e:
        return {"error": str(e)}

@app.post("/tasks")
async def create_task(task: Task):
    try:
        print(table)
        table.put_item(Item=task.dict())
        return {"message": "Task created successfully"}
    except Exception as e:
        return {"error": str(e)}
