from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from os import environ
from flask_cors import CORS
import os
import sys

import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = (  
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr_database"  
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    
@app.route("/ticket")
def get_all():
    ticket_list = db.session.scalars(db.select(Ticket)).all()
    if len(ticket_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tickets": [individual_ticket.json() for individual_ticket in ticket_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404, 
            "message": "There are no tickets."
        }
    ), 404


@app.route("/ticket/EID/<string:EID>")
def get_tickets_by_eid(EID):
    ticket_list = db.session.scalars(db.select(Ticket).filter_by(EID=EID)).all()
    if len(ticket_list):
        return jsonify(
            {
                "code": 201,
                "data": [individual_ticket.json() for individual_ticket in ticket_list]
            }
        )
    return jsonify({"code": 404, "message": "There are no tickets for this event."}), 404

# ticket no longer contains UID

# @app.route("/ticket/UID/<string:UID>")
# def get_tickets_by_uid(UID):
#     ticket_list = db.session.scalars(db.select(Ticket).filter_by(UID=UID)).all()
#     if len(ticket_list):
#         return jsonify(
#             {
#                 "code": 201,
#                 "data": [individual_ticket.json() for individual_ticket in ticket_list]
#             }
#         )
#     return jsonify({"code": 404, "message": "There are no tickets for this user."}), 404

# combine - UID,EID
# @app.route("/ticket/EID/<int:eid>/UID/<int:uid>")  
# def get_ticket_by_uid_eid(uid, eid):
#     ticket = Ticket.query.filter_by(UID=uid, EID=eid).first()

#     if ticket:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": ticket.json()
#             }
#         )
    
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Ticket not found."
#         }
#     ), 404



# POST - create ticket
@app.route("/ticket/<string:TicketID>", methods=["POST"])
def create_ticket(TicketID):

    eid = request.get_json().get("EID")
    uid = request.get_json().get("UID")
    tier = request.get_json().get("Tier")
    PriceID = request.get_json().get("PriceID")

    ticket = Ticket(
        TicketID,
        eid,
        uid,
        tier,
        PriceID
    )

    try:
        db.session.add(ticket)
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
                "message": "An error occured while creating the ticket. " +str(e)
            }
        ), 500
    
    print(json.dumps(ticket.json(), default=str))


    return jsonify(
        {
            "code": 201,
            "data": ticket.json()
        }
    ), 201

@app.route("/userticket", methods=["POST"])
def create_userticket():

    TicketID = request.get_json().get("TicketID")
    UID = request.get_json().get("UID")

    user_ticket = UserTicket(
        UID,
        TicketID
    )

    try:
        db.session.add(user_ticket)
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
                "message": "An error occured while creating the ticket. " +str(e)
            }
        ), 500
    
    print(json.dumps(user_ticket.json(), default=str))


    return jsonify(
        {
            "code": 201,
            "data": user_ticket.json()
        }
    ), 201

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage event ...")
    app.run(host='0.0.0.0', port=5008, debug=True)