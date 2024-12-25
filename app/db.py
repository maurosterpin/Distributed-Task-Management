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

TASK_TABLE_NAME = 'task_table'
USER_TABLE_NAME = 'user_table'

create_table(TASK_TABLE_NAME)
create_table(USER_TABLE_NAME)

task_table = dynamodb.Table(TASK_TABLE_NAME)
user_table = dynamodb.Table(USER_TABLE_NAME)