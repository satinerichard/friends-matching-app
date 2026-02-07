from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

MOCK_DATABASE_USERS = []

#tell what a user looks like
class User(BaseModel):
    id: int = None
    username: str
    email: str
    full_name: str
    place_of_birth: str
    school: str
    city: str
    age: int
    interests: List[str]

#class Location(BaseModel):
 #   longitude: float
  #  latitude: float


@app.get("/")
def root():
    return {'message': 'Friender'}

@app.post("/add_user")
def add_user(user: User):
    MOCK_DATABASE_USERS.append(user)
    return {'message': 'User added!' , 'user':user }

@app.get("/people")
def get_people(my_name: str):
    # show all users except yourself
    others =[]
    for user in MOCK_DATABASE_USERS:
        if user.username != my_name:
            others.append(user)
    return {'people': others}


# create the like/dislike buttons 
actions = []

class Action(BaseModel):
    on_who: str
    liked_by: str
    liked: bool

@app.post("/button")
def button(action: Action):
    actions.append(action)
    return {'message': 'Action recorded!' , 'action': action } 
    print(f"{action.on_who} got {'❤️' if action.liked else '❌'}")
    
    if action.liked:
        return {"message": "❤️ LIKED!"}
    return {"message": "❌ PASSED"}



