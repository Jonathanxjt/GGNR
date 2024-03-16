from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from os import environ
# from flask_cors import CORS
import os
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db =SQLAlchemy(app)

# CORS(app)

class User(db.Model):
    __tablename__ = 'users'
    
    UID = db.Column(db.Integer, primary_key=True)
    preferences = db.Column(db.Text)
    
    # Relationships
    attendees = relationship('Attendee', back_populates='user')
    tickets = relationship('Ticket', back_populates='user')

    def __init__(self, UID, preferences):
        self.UID = UID
        self.preferences = preferences
    
    def to_json(self):
        return {
            'UID': self.UID,
            'preferences': self.preferences
        }
    
# GET all users
@app.route("/user")
def get_all():
    user_list = db.session.scalars(db.select(User)).all()

    if len(user_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in user_list]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "User list not found."
        }
    ), 404


# GET user by uid
@app.route("/user/<string:UID>")
def get_user_by_uid(UID):
    user = db.session.scalar(db.select(User).filter_by(UID=UID).limit(1)).first()

    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There is no user."
        }
    ), 404

# change port?
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)