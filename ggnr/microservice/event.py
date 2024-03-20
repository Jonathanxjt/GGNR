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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
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
    UID = db.Column(db.Integer, ForeignKey('users.UID'))
    Tier = db.Column(db.SmallInteger)
    Price = db.Column(db.Float)
    
    # Relationships
    event = relationship('Event', back_populates='tickets')
    user = relationship('User', back_populates='tickets')
    def __init__(self, TicketID, EID, UID, Tier, Price):
        self.TicketID = TicketID
        self.EID = EID
        self.UID = UID
        self.Tier = Tier
        self.Price = Price
    
    def json(self):
        return {
            'TicketID': self.TicketID,
            'EID': self.EID,
            'UID': self.UID,
            'Tier': self.Tier,
            'Price': self.Price
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
    Price = db.Column(db.Float(precision=2))
    
    # Relationships
    attendees = relationship('Attendee', back_populates='event')
    tickets = relationship('Ticket', back_populates='event')

    def __init__(self, EID, TierID, Title, Description, EventLogo, GameName, GameLogo, Location, Time, GameCompany, Capacity, Price):
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
        self.Price = Price

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
            "Price": self.Price
        }

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
    
    def json(self):
        return {
            'UID': self.UID,
            'preferences': self.preferences
        }
        
# GET ALL
@app.route("/event")
def get_all():
    eventlist = db.session.scalars(db.select(Event)).all()
    if len(eventlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "events": [event.json() for event in eventlist]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no events."
        }
    ), 404


# GET EID
@app.route("/event/<string:EID>")
def find_by_event_id(EID):
    event = db.session.scalars(db.select(Event).filter_by(EID=EID).limit(1)).first()
    if event:
        return jsonify(
            {
                "code": 200,
                "data": event.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "EID": EID
            },
            "message": "Event not found."
        }
    ), 404

# GET - games name
@app.route("/event/gamename/<string:gamename>")
def find_by_gamename(gamename):
    event_list = db.session.scalars(db.select(Event).filter_by(GameName=gamename)).all()
    if len(event_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "events": [event.json() for event in event_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no events."
        }
    ), 404

# POST - create event
@app.route("/event", methods=["POST"])
def create_event():
    EID = request.json.get("EID")
    TierID = request.json.get("TierID")
    Title = request.json.get("Title")
    Description = request.json.get("Description")
    EventLogo = request.json.get("EventLogo")
    GameName = request.json.get("GameName")
    GameLogo = request.json.get("GameLogo") 
    Location = request.json.get("Location")
    Time = request.json.get("Time")
    GameCompany = request.json.get("GameCompany")
    Capacity = request.json.get("Capacity")
    Price = request.json.get("Price")


    event = Event(
        EID = EID,
        TierID = TierID,
        Title = Title,
        Description = Description,
        EventLogo = EventLogo,
        GameName = GameName,
        GameLogo = GameLogo,
        Location = Location,
        Time = Time,
        GameCompany = GameCompany,
        Capacity = Capacity,
        Price = Price,
    )

    try:
        db.session.add(event)
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
                "message": "An error occured while creating the event. " +str(e)
            }
        ), 500
    
    print(json.dumps(event.json()), default=str)

    return jsonify(
        {
            "code": 201,
            "data": event.json()
        }
    ), 201

# PUT - edit event's Time or Price or Location
@app.route("/event/<string:EID>", methods=['PUT'])
def update_event(EID):
    try:
        event = db.session.scalars(db.select(Event).filter_by(EID=EID).limit(1)).first()
        if not event:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "EID": EID
                    },
                    "message": "event not found."
                }
            ), 404

        # update Time or Price or Location
        # data = request.get_json()
        time = request.get_json().get("Time")
        px = request.get_json().get("Price")
        location = request.get_json().get("Location")
        capacity = request.get_json().get("Capacity")

        if time != None:
            event.Time = time
            # db.session.commit()
            # return jsonify(
            #     {
            #         "code": 200,
            #         "data": event.json()
            #     }
            # ), 200
        
        if px != None:
            event.Price = px
            # db.session.commit()
            # return jsonify(
            #     {
            #         "code": 200,
            #         "data": event.json()
            #     }
            # ), 200
        
        if location != None:
            event.Location = location
            # db.session.commit()
            # return jsonify(
            #     {
            #         "code": 200,
            #         "data": event.json()
            #     }
            # ), 200
        
        if capacity != None:
            event.Capacity -= int(capacity)
            # db.session.commit()
            # return jsonify(
            #     {
            #         "code": 200,
            #         "data": event.json()
            #     }
            # ), 200
        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": event.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "EID": EID
                },
                "message": "An error occurred while updating the event. " + str(e)
            }
        ), 500
    

# delete event
@app.route("/event/<string:EID>", methods=["DELETE"])
def delete_event(EID):
    event = db.session.scalars(db.select(Event).filter_by(EID=EID).limit(1)).first()

    if not event:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "EID": EID
                },
                "message": "Event not found."
            }
        ), 400
    
    try:
        db.session.delete(event)
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
                "data": {"EID": EID},
                "message": "An unexpected error occurred deleting the event. " + ex_str,
            }
        ), 500
    
    return jsonify({"code": 201, "EID": EID}), 201


# may change port number
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage event ...")
    app.run(host='0.0.0.0', port=5000, debug=True)