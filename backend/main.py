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
    for prev_action in actions:
        if (prev_action.on_who == action.liked_by and    # They liked me
            prev_action.liked_by == action.on_who and     # I liked them  
            prev_action.liked and action.liked):           # Both liked
            return {"message": "🎉 MATCH!", "friend": action.on_who}
    
    return {'message': 'Action recorded!', 'action': action} 


@app.get("/matches")
def get_matches(my_name: str):
    matches=[]
    
    # I liked them
    my_likes = [a for a in actions if a.liked_by == my_name and a.liked]
    
    for like in my_likes:
        # Did they like back?
        their_like = [a for a in actions 
                     if a.on_who == my_name and 
                        a.liked_by == like.on_who and 
                        a.liked]
        if their_like:
            matches.append(like.on_who)
    
    return {'matches': matches}



