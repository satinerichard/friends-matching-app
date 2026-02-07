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



@app.route("/swipes", methods=["POST"])
def swipe_route():
    data = request.json

    swiper_id = data.get("swiper_id")
    swiped_id = data.get("swiped_id")
    direction = data.get("direction")
    
    


    if not swiper_id or not swiped_id or direction not in ["right", "left"]:
        return jsonify({"message": "Invalid input"}), 400

    if not User.query.get(swiper_id) or not User.query.get(swiped_id):
        return jsonify({"message": "User not found"}), 404

    # Prevent a user from swiping themselves
    if swiper_id == swiped_id:
        return jsonify({"message": "Cannot swipe on yourself"}), 400

    existing_swipe = Swipe.query.filter_by(swiper_id=swiper_id, swiped_id=swiped_id).first()
    if existing_swipe:
        existing_swipe.direction = direction
        db.session.commit()
        message = "Swipe updated"
    else:
        swipe = Swipe(swiper_id=swiper_id, swiped_id=swiped_id, direction=direction)
        db.session.add(swipe)
        db.session.commit()
        message = "Swipe recorded"

    # check for mutual right swipe to create a match
    if direction == "right":
        mutual_swipe = Swipe.query.filter_by(
            swiper_id=swiped_id, 
            swiped_id=swiper_id, 
            direction="right"
        ).first()
        if mutual_swipe:
            # check if match already exists
            existing_match = Match.query.filter(((Match.user1_id==swiper_id) & (Match.user2_id==swiped_id)) |
                ((Match.user1_id==swiped_id) & (Match.user2_id==swiper_id))
            ).first()
            if not existing_match:
                match = Match(user1_id=swiper_id, user2_id=swiped_id)
                db.session.add(match)
                db.session.commit()
                return jsonify({"message" : "It's a match!", "match":{"user1_id" : swiper_id, "user2_id": swiped_id}})

    return jsonify({"message": message})


if __name__ == "__main__":
    app.run(debug=True)
