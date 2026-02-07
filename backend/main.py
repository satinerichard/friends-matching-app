from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

#tell what a user looks like
class User(BaseModel):
    username: str
    email: str
    full_name: str
    place_of_birth: str
    school: str
    city: str
    age: int
    interests: List[str]

class Location(BaseModel):
    longitude: float
    latitude: float

@app.get("/")
def root():
    return {'message': 'Hello World'}

@app.get("/users")
def read_users():
    return MOCK_DATABASE_USERS

@app.post("/user")
def create_users(user_data: User):

    MOCK_DATABASE_USERS.append(user_data)
    return {'message': 'User created successfully', 'user': user_data}

MOCK_DATABASE_USERS = []


