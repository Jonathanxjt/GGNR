from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from os import environ
from flask_cors import CORS
import os
import sys

import bcrypt

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = ( 
#     environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr_database" 
# )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db =SQLAlchemy(app)

CORS(app)

class Attendee(db.Model):
    __tablename__ = 'attendees'
    
    AID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    EID = db.Column(db.Integer, ForeignKey('events.EID'))
    UID = db.Column(db.Integer, ForeignKey('users.UID'))
    ticketID = db.Column(db.Integer)
    transactionID = db.Column(db.Integer)
    
    # Relationships
    event = relationship('Event', back_populates='attendees')
    user = relationship('User', back_populates='attendees')
    def __init__(self, EID, UID, ticketID, transactionID):
        self.EID = EID
        self.UID = UID
        self.ticketID = ticketID
        self.transactionID = transactionID
    
    def json(self):
        return {
            'AID': self.AID,
            'EID': self.EID,
            'UID': self.UID,
            'ticketID': self.ticketID,
            'transactionID': self.transactionID
        }
    

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    TicketID = db.Column(db.Integer, primary_key=True)
    EID = db.Column(db.Integer, ForeignKey('events.EID'))
    TierID = db.Column(db.SmallInteger)
    PriceID = db.Column(db.String(255))
    
    # Relationships
    event = relationship('Event', back_populates='tickets')
    user_tickets = relationship('UserTicket', back_populates='tickets')
    def __init__(self, TicketID, EID, UID, TierID, PriceID):
        self.TicketID = TicketID
        self.EID = EID
        self.UID = UID
        self.TierID = TierID
        self.PriceID = PriceID
    
    def json(self):
        return {
            'TicketID': self.TicketID,
            'EID': self.EID,
            'TierID': self.TierID,
            'PriceID': self.PriceID
        }

class Event(db.Model):
    __tablename__ = 'events'
    
    EID = db.Column(db.Integer, primary_key=True)
    TierID = db.Column(db.SmallInteger, primary_key=True)
    Title = db.Column(db.String(255))
    Description = db.Column(db.Text)
    EventLogo = db.Column(db.Text)
    GameName = db.Column(db.String(255))
    GameLogo = db.Column(db.Text)
    Location = db.Column(db.String(255))
    Time = db.Column(db.DateTime)
    GameCompany = db.Column(db.String(255))
    Capacity = db.Column(db.Integer)
    PriceID = db.Column(db.String(255))
    
    # Relationships
    attendees = relationship('Attendee', back_populates='event')
    tickets = relationship('Ticket', back_populates='event')

    def __init__(self, EID, TierID, Title, Description, EventLogo, GameName, GameLogo, Location, Time, GameCompany, Capacity, PriceID):
        self.EID = EID
        self.TierID = TierID
        self.Title = Title
        self.Description = Description
        self.EventLogo = EventLogo
        self.GameName = GameName
        self.GameLogo = GameLogo
        self.Location = Location
        self.Time = Time
        self.GameCompany = GameCompany
        self.Capacity = Capacity
        self.PriceID = PriceID

    def json(self):
        return {
            "EID": self.EID,
            "TierID": self.TierID,
            "Title": self.Title,
            "Description": self.Description,
            "EventLogo": self.EventLogo,
            "GameName": self.GameName,
            "GameLogo": self.GameLogo,
            "Location": self.Location,
            "Time": self.Time.isoformat() if self.Time else None,  # ISO formatting for dateTime
            "GameCompany": self.GameCompany,
            "Capacity": self.Capacity,
            "PriceID": self.PriceID
        }

class User(db.Model):
    __tablename__ = 'users'

    UID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences = db.Column(db.Text)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    organiser = db.Column(db.Boolean, nullable=False)
    organiser_company = db.Column(db.String(255))
    
    # Relationships
    attendees = relationship('Attendee', back_populates='user')
    user_tickets = relationship('UserTicket', back_populates='user')

    def __init__(self, username, password_hash, preferences, email, contact, organiser, organiser_company):
        self.username = username
        self.password_hash = password_hash
        self.preferences = preferences
        self.email = email
        self.contact = contact
        self.organiser = organiser
        self.organiser_company = organiser_company
    
    def json(self):
        return {
            'UID': self.UID,
            'username': self.username,
            'preferences': self.preferences,
            'email': self.email,
            'contact': self.contact,
            'organiser': self.organiser,
            'organiser_company': self.organiser_company
        }
        
class UserTicket(db.Model):
    __tablename__ = 'user_tickets'

    UID = db.Column(db.Integer, ForeignKey('users.UID'), primary_key=True)
    TicketID = db.Column(db.Integer, ForeignKey('tickets.TicketID'), primary_key=True)

    # Relationships
    user = relationship('User', back_populates='user_tickets')
    tickets = relationship('Ticket', back_populates='user_tickets')

    def __init__(self, UID, TicketID):
        self.UID = UID
        self.TicketID = TicketID

    def json(self):
        return {
            'UID': self.UID,
            'TicketID': self.TicketID
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
@app.route("/user/<int:UID>")
def get_user_by_uid(UID):
    user = db.session.scalars(db.select(User).filter_by(UID=UID).limit(1)).first()
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

# GET password - check password
@app.route("/user/check-password/<string:email>/password/<string:input>")
def check_password(email,input):
    user = db.session.query(User).filter_by(email=email).first()

    if user:

        entered_pw_bytes = input.encode("utf-8")
        hashed_password = user.password_hash.encode("utf-8")

        if bcrypt.checkpw(entered_pw_bytes, hashed_password):
            return jsonify(
                {
                    "code": 200,
                    "message": "Correct password",
                    "data" : user.json()
                }
            )
        else:
            return jsonify(
                {
                    "code":200,
                    "message": "Incorrect password"
                }
            )
    
    return jsonify(
        {
            "code": 404,
            "message": "There is no user."
        }
    ), 404

# GET - all email
@app.route("/user/email")
def get_all_emails():
    user = db.session.scalars(db.select(User)).all()

    if user:
        email_list = []
        for obj in user:
            email_list.append(obj.email)
        return jsonify(
            {
                "code": 200,
                "data" : email_list
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "Username list not found"
        }
    ),404

# GET - contact information (for notifications.py only)
@app.route("/user/contact-information")
def get_contact_information():
    attendee_list = request.get_json().get("attendee_list")

    uid_list = []
    for obj in attendee_list:
        uid_list.append(obj["UID"])

    user_list = db.session.query(User).filter(User.UID.in_(uid_list)).all()

    if user_list:
        return jsonify(
            {
                "code": 200,
                "data": [user.json() for user in user_list]
            }
        )

    # if fail
    return jsonify(
        {
            "code": 404,
            "message": "Contact infromation not found."
        }
    ), 404

# POST - create user
@app.route("/user/create_user", methods=["POST"])
def create_user():
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    preferences = request.get_json().get("preferences")
    email = request.get_json().get("email")
    contact = request.get_json().get("contact")
    organiser = request.get_json().get("organiser")
    organiser_company = request.get_json().get("organiser_com")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        username=username,
        password_hash=hashed_password.decode('utf-8'),  # Store the hashed password as a string
        preferences=preferences,
        email=email,
        contact=contact,
        organiser=organiser,
        organiser_company=organiser_company
    )

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = (
            str(e)
            + " at "
            + str(exc_type)
            + ": "
            + fname
            + ": line "
            + str(exc_tb.tb_lineno)
        )
        print(ex_str)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the user. " + str(e)
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

# PUT - edit user's preference
@app.route("/user/edit_preference/<string:UID>", methods=["PUT"])
def edit_user_preference(UID):
    try:
        user = db.session.scalars(db.select(User).filter_by(UID=UID).limit(1)).first()
        if not user:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "UID": UID
                    },
                    "message": "User not found."
                }
            ), 404
        
        # Get the new preferences from the request body
        new_preferences = request.get_json().get("preferences", "")

        # Update the user's preferences
        user.preferences = new_preferences

        # Commit the changes to the database
        db.session.commit()

        return jsonify(
            {
                "code": 201,
                "data": user.json()
            }
        ), 201
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UID": UID
                },
                "message": "An error occurred while updating user preferences. " + str(e)
            }
        ), 500


    
# GET - get list of users whose preferences align with GameName
@app.route("/user/user_preference_gamename")
def get_user_preference_gamename():
    # update the function
    gamename = request.get_json().get("GameName")
    user_list = db.session.scalars(db.select(User)).all()

    if len(user_list):

        output = []
        for obj in user_list:
            preference_str = obj.preferences
            preference_list = preference_str.split(",")

            if gamename in preference_list:
                output.append(obj)

        return jsonify(
            {
                "code": 200,
                "data": [user.json() for user in output]
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "User list not found."
        }
    ), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)