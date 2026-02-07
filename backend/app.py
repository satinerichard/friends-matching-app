# this creates a file friendR.db in my backend folder to store all users
from flask import Flask, request, jsonify
from models import db, User

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
    data = request.json  # jason is a text format used to store an exchange data

user_id = data.get("id")
username = data.get("username")
real_name = data.get("real_name")
age = data.get("age")
email = data.get("email")
bio = data.get("bio")
birth_place = data.get("birth_place")
interests = data.get("interests")

user, message = add_or_update_user(
    user_id = user_id,
    username = username,
    real_name = real_name,
    age=age,
    email=email,
    bio=bio,
    birth_place = birth_place,
    interests = interests
)
    

if not user:
        return jsonify({"message": message}), 404

    # Return user info
    return jsonify({
        "message": message,
        "user": {
            "id": user.id,
            "name": user.name,
            "real_name": user.real_name,
            "email": user.email,
            "age": user.age,
            "bio": user.bio,
            "place_birth": user.place_birth,
            "interests": user.interests
            
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
