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

TABLE_NAME = 'user_table'
create_table(TABLE_NAME)
table = dynamodb.Table(TABLE_NAME)

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

def get_user(user_id: str):
    try:
        response = table.get_item(Key={'id': user_id})
        return response.get('Item', None)
    except Exception as e:
        raise Exception(f"Error retrieving user: {str(e)}")

def create_user(user: User):
    try:
        table.put_item(Item=user.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")
