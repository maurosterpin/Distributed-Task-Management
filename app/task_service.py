from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://host.docker.internal:4566",
    region_name='us-east-1',
    aws_access_key_id="access_key_id",
    aws_secret_access_key="secret"
)

def create_table(table_name):
    try:
        print(f"Creating table '{table_name}'...")
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Table created successfully!")
    except Exception as e:
        print(f"Table creation error: {str(e)}")

TABLE_NAME = 'task_table'
create_table(TABLE_NAME)
table = dynamodb.Table(TABLE_NAME)

class Task(BaseModel):
    id: str
    title: str
    desc: str
    owner: str
    assignee: str
    status: str

def get_task(task_id: str):
    try:
        response = table.get_item(Key={'id': task_id})
        return response.get('Item', None)
    except Exception as e:
        raise Exception(f"Error retrieving task: {str(e)}")

def create_task(task: Task):
    try:
        table.put_item(Item=task.dict())
        return {"message": "Task created successfully"}
    except Exception as e:
        raise Exception(f"Error creating task: {str(e)}")
