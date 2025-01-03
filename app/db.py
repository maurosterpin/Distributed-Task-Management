import boto3
from dotenv import load_dotenv
import os

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DB_ENDPOINT_URL"),
    region_name=os.getenv("DB_REGION_NAME"),
    aws_access_key_id=os.getenv("DB_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("DB_SECRET_ACCESS_KEY")
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

TASK_TABLE_NAME = 'task_table'
USER_TABLE_NAME = 'user_table'

create_table(TASK_TABLE_NAME)
create_table(USER_TABLE_NAME)

task_table = dynamodb.Table(TASK_TABLE_NAME)
user_table = dynamodb.Table(USER_TABLE_NAME)