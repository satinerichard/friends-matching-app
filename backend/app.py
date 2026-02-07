# this creates a file friendR.db in my backend folder to store all users
from flask import Flask, request, jsonify
from models import *

app = Flask(__name__)

# Connect database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friendR.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables (only runs once)
with app.app_context():
    db.create_all()


@app.route("/users", methods=["POST"])
def add_or_update_user_route():
    data = request.json

    user_id = data.get("id")
    username = data.get("username")
    real_name = data.get("real_name")
    age = data.get("age")
    email = data.get("email")
    bio = data.get("bio")
    birth_place = data.get("birth_place")
    interests = data.get("interests")

    user, message = add_or_update_user(
        user_id=user_id,
        username=username,
        real_name=real_name,
        age=age,
        email=email,
        bio=bio,
        birth_place=birth_place,
        interests=interests
    )

    if not user:
        return jsonify({"message": message}), 404

    return jsonify({
        "message": message,
        "user": {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "age": user.age,
            "email": user.email,
            "bio": user.bio,
            "birth_place": user.birth_place,
            "interests": user.interests
        }
    })
