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
