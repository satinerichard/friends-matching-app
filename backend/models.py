from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True) # creates a unique identifier fro each user
  name = db.Column(db.String, unique=True) # each user needs a UNIQUE username
  age = db.COlumn(db.Integer)
  
