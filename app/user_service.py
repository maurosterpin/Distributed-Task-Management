from pydantic import BaseModel
from .db import user_table

class User(BaseModel):
    id: str
    name: str
    email: str

def get_user(user_id: str) -> User:
    try:
        response = user_table.get_item(Key={'id': user_id})
        item = response.get('Item', None)
        if item is None:
            raise Exception(f"User with id '{user_id}' does not exist.")
        return User(**item)
    except Exception as e:
        raise Exception(f"Error retrieving user: {str(e)}")

def upsert_user(user: User) -> dict:
    try:
        user_table.put_item(Item=user.dict())
        return {"message": "User upserted successfully"}
    except Exception as e:
        raise Exception(f"Error upserting user: {str(e)}")
