from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True) # creates a unique identifier for each user
  username = db.Column(db.String(100), unique=True, nullable=False) # each user needs a UNIQUE username
  real_name = db.Column(db.String(100), nullable=False) # legal name
  email = db.Column(db.String(100), unique=True, nullable=False)
  age = db.Column(db.Integer)
  bio = db.Column(db.String(300))
  birth_place = db.Column(db.String(300))
  interests = db.Column(db.String(500))


  

def add_or_update_user(user_id=None, username=None, real_name=None, age=None, email=None, bio=None, birth_place=None, interests=None):

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None, "User not found"
        message = "User updated"
    else:
        # create new user with given info
        user = User()
        db.session.add(user)
        message = "User created"

    # Update only provided fields
    if username is not None:
        user.username = username
    if real_name is not None:
        user.real_name = real_name
    if age is not None:
        user.age = age
    if email is not None:
        user.email = email
    if bio is not None:
        user.bio = bio
    if birth_place is not None:
        user.birth_place = birth_place
    if interests is not None:
        user.interests = interests

    db.session.commit()
    return user, message


class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swiper_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    swiped_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    direction = db.Column(db.String(10), nullable=False) #right or left
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)



class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)