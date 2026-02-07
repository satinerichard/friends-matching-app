# this creates a file friendR.db in my backend folder to store all users
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import *    

app = Flask(__name__, 
    template_folder="../frontend",   # HTML files
    static_folder="../frontend"      # CSS and JS
    )

# Connect database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friendR.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables (only runs once)
with app.app_context():
    db.create_all()


# --- Serve pages ---
@app.route("/")
def home():
    return render_template("website_hack.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/connect")
def connect_page():
    return render_template("connecting.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    real_name = data.get("fullname")

    # create user
    user, message = add_or_update_user(
        username=username,
        email=email,
        real_name=real_name
        # you can hash password later
    )

    if not user:
        return render_template("signup.html", error=message)

    return redirect(url_for("login_page"))

@app.route("/login", methods=["POST"])
def login():
    data = request.form
    username = data.get("username")
    # check if username exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template("login.html", error="User not found")
    
    # store user id in session for later (optional)
    return redirect(url_for("connect_page"))




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

@app.route("/people", methods=["GET"])
def get_people():
    my_username = request.args.get("my_name")

    if not my_username:
        return jsonify({"message": "Missing my_name"}), 400

    users = User.query.filter(User.username != my_username).all()

    return jsonify({
        "people": [
            {
                "id": u.id,
                "username": u.username,
                "real_name": u.real_name,
                "age": u.age,
                "birth_place": u.birth_place,
                "interests": u.interests.split(",") if u.interests else []
            }
            for u in users
        ]
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



@app.route("/matches", methods=["GET"])
def get_matches():
    username = request.args.get("my_name")

    if not username:
        return jsonify({"message": "Missing my_name"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    matches = Match.query.filter(
        (Match.user1_id == user.id) |
        (Match.user2_id == user.id)
    ).all()

    result = []
    for m in matches:
        other_id = m.user2_id if m.user1_id == user.id else m.user1_id
        other_user = User.query.get(other_id)
        result.append({
            "id": other_user.id,
            "username": other_user.username,
            "real_name": other_user.real_name
        })

    return jsonify({"matches": result})



if __name__ == "__main__":
    app.run(debug=True)
