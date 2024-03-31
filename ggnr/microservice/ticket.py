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
    
    # Relationships
    event = relationship('Event', back_populates='attendees')
    user = relationship('User', back_populates='attendees')
    def __init__(self, EID, UID, ticketID):
        self.EID = EID
        self.UID = UID
        self.ticketID = ticketID

    
    def json(self):
        return {
            'AID': self.AID,
            'EID': self.EID,
            'UID': self.UID,
            'ticketID': self.ticketID
        }
    

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    TicketID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Set autoincrement to True
    EID = db.Column(db.Integer, ForeignKey('events.EID'))
    TierID = db.Column(db.SmallInteger)
    PriceID = db.Column(db.String(255))
    
    # Relationships
    event = relationship('Event', back_populates='tickets')
    user_tickets = relationship('UserTicket', back_populates='tickets')

    def __init__(self, EID, TierID, PriceID):
        self.EID = EID
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
    Title = db.Column(db.String(255))
    Description = db.Column(db.Text)
    EventLogo = db.Column(db.Text)
    GameName = db.Column(db.String(255))
    GameLogo = db.Column(db.Text)
    Location = db.Column(db.String(255))
    Time = db.Column(db.DateTime)
    organiser_company = db.Column(db.String(255))

    # Relationships
    event_types = relationship('Event_type', back_populates='event')
    attendees = relationship('Attendee', back_populates='event')
    tickets = relationship('Ticket', back_populates='event')

    def __init__(self, Title, Description, EventLogo, GameName, GameLogo, Location, Time, organiser_company):
        self.Title = Title
        self.Description = Description
        self.EventLogo = EventLogo
        self.GameName = GameName
        self.GameLogo = GameLogo
        self.Location = Location
        self.Time = Time
        self.organiser_company = organiser_company

    def json(self):
        return {
            "EID": self.EID,
            "Title": self.Title,
            "Description": self.Description,
            "EventLogo": self.EventLogo,
            "GameName": self.GameName,
            "GameLogo": self.GameLogo,
            "Location": self.Location,
            "Time": self.Time.isoformat() if self.Time else None,  # ISO formatting for dateTime
            "organiser_company": self.organiser_company,
        }

class Event_type(db.Model):
    __tablename__ = 'events_type'

    EID = db.Column(db.Integer, db.ForeignKey('events.EID'), primary_key=True)
    TierID = db.Column(db.SmallInteger, primary_key=True)
    Category = db.Column(db.String(255))
    Capacity = db.Column(db.Integer)
    Price = db.Column(db.Float)
    PriceID = db.Column(db.String(255))

    # Relationships
    event = relationship('Event', back_populates='event_types')

    def __init__(self, TierID, Category, Price, Capacity, PriceID):
        self.TierID = TierID
        self.Category = Category
        self.Capacity = Capacity
        self.PriceID = PriceID
        self.Price = Price

    def json(self):
        return {
            "TierID": self.TierID,
            "Category": self.Category,
            "Capacity": self.Capacity,
            "PriceID": self.PriceID,
            "Price": self.Price,
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

# Get tickets based on the user ID
@app.route("/ticket/<int:uid>", methods=["GET"])
def get_user_tickets(uid):
    user_tickets = db.session.scalars(db.select(UserTicket).filter_by(UID=uid)).all()
    if not user_tickets:
        return jsonify({"code": 404, "message": "No tickets found for this user."}), 404

    tickets = []
    for user_ticket in user_tickets:
        ticket = db.session.get(Ticket, user_ticket.TicketID)
        if ticket:
            tickets.append(ticket.json())

    return jsonify({"code": 200, "data": tickets}), 200



# POST - create ticket
@app.route("/ticket", methods=["POST"])
def create_ticket():
    eid = request.get_json().get("EID")
    tier = request.get_json().get("TierID")
    price_id = request.get_json().get("PriceID")
    uid = request.get_json().get("UID")

    # Create a new Ticket
    ticket = Ticket(
        EID=eid,
        TierID=tier,
        PriceID=price_id
    )

    try:
        db.session.add(ticket)
        db.session.flush()  # Flush the changes to get the generated TicketID

        # Create a new UserTicket
        user_ticket = UserTicket(
            UID=uid,
            TicketID=ticket.TicketID
        )
        db.session.add(user_ticket)

        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": {
                    "ticket": ticket.json(),
                    "user_ticket": user_ticket.json()
                }
            }
        ), 201
    except Exception as e:
        db.session.rollback()
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
                "message": "An error occurred while creating the ticket. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage event ...")
    app.run(host='0.0.0.0', port=5008, debug=True)