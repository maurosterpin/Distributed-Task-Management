from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
from .db import user_table

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

def get_user(user_id: str) -> User:
    try:
        response = user_table.get_item(Key={'id': user_id})
        item = response.get('Item', None)
        return User(**item)
    except Exception as e:
        raise Exception(f"Error retrieving user: {str(e)}")

def create_user(user: User) -> dict:
    try:
        user_table.put_item(Item=user.dict())
        return {"message": "User upserted successfully"}
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")
