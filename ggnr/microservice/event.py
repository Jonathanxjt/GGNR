from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from os import environ
from flask_cors import CORS
import os
import sys

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ( 
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr_database" 
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CORS(app)

# * ORM Classes
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


# GET ALL events with their types
@app.route("/event")
def get_all():
    # Get all events and their related types using joined loading
    eventlist = db.session.query(Event).options(db.joinedload(Event.event_types)).all()
    
    # Check if the event list is not empty
    if eventlist:
        events_data = []
        for event in eventlist:
            # Serialize the Event object
            event_data = {
                "EID": event.EID,
                "Title": event.Title,
                "Description": event.Description,
                "EventLogo": event.EventLogo,
                "GameName": event.GameName,
                "GameLogo": event.GameLogo,
                "Location": event.Location,
                "Time": event.Time.isoformat() if event.Time else None,
                "organiser_company": event.organiser_company,
                "event_types": []
            }

            # Serialize associated Event_type objects
            for etype in event.event_types:
                event_data['event_types'].append({
                    "EID": etype.EID,
                    "TierID": etype.TierID,
                    "Category": etype.Category,
                    "Capacity": etype.Capacity,
                    "Price": etype.Price,
                    "PriceID": etype.PriceID
                })
            
            # Add the serialized Event with its types to the events_data list
            events_data.append(event_data)
        
        # Return the JSON response with all events and their types
        return jsonify(
            {
                "code": 200,
                "data": {
                    "events": events_data
                }
            }
        )
    
    # If no events were found, return a 404 response
    return jsonify(
        {
            "code": 404,
            "message": "There are no events."
        }
    ), 404


# GET - Retrieve a specific event by title and its event_types
@app.route("/get_event/<title>", methods=["GET"])
def get_event(title):
    event = Event.query.filter_by(Title=title).first()
    if event:
        # Serialize the Event object
        event_data = {
            "EID": event.EID,
            "Title": event.Title,
            "Description": event.Description,
            "EventLogo": event.EventLogo,
            "GameName": event.GameName,
            "GameLogo": event.GameLogo,
            "Location": event.Location,
            "Time": event.Time.isoformat() if event.Time else None,
            "organiser_company": event.organiser_company,
            "event_types": []
        }

        # Serialize associated Event_type objects
        for etype in event.event_types:
            event_data['event_types'].append({
                "EID": etype.EID,
                "TierID": etype.TierID,
                "Category": etype.Category,
                "Capacity": etype.Capacity,
                "Price": etype.Price,
                "PriceID": etype.PriceID
            })

        return jsonify({"code": 200, "data": event_data}), 200
    else:
        return jsonify({"code": 404, "message": "Event not found"}), 404

# GET EID
@app.route("/event/<string:EID>")
def find_by_event_id(EID):
    event = Event.query.filter_by(EID=EID).first()
    if event:
        # Serialize the Event object
        event_data = {
            "EID": event.EID,
            "Title": event.Title,
            "Description": event.Description,
            "EventLogo": event.EventLogo,
            "GameName": event.GameName,
            "GameLogo": event.GameLogo,
            "Location": event.Location,
            "Time": event.Time.isoformat() if event.Time else None,
            "organiser_company": event.organiser_company,
            "event_types": []
        }

        # Serialize associated Event_type objects
        for etype in event.event_types:
            event_data['event_types'].append({
                "EID": etype.EID,
                "TierID": etype.TierID,
                "Category": etype.Category,
                "Capacity": etype.Capacity,
                "Price": etype.Price,
                "PriceID": etype.PriceID
            })

        return jsonify({"code": 200, "data": event_data}), 200
    else:
        return jsonify({"code": 404, "message": "Event not found"}), 404


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

@app.route("/event/gamecompany/<string:gamecompany>")
def find_by_gamecompany(gamecompany):
    event_list = db.session.scalars(db.select(Event).filter_by(GameCompany=gamecompany)).all()
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
@app.route("/create_event", methods=["POST"])
def create_event():
    # Event details
    Title = request.json.get("Title")
    Description = request.json.get("Description")
    EventLogo = request.json.get("EventLogo")
    GameName = request.json.get("GameName")
    GameLogo = request.json.get("GameLogo")
    Location = request.json.get("Location")
    Time = request.json.get("Time")
    organiser_company = request.json.get("organiser_company")

    # Convert Time from string to datetime object
    # Time = datetime.strptime(Time, '%Y-%m-%d %H:%M:%S') if Time else None

    # Create Event
    event = Event(
        Title=Title,
        Description=Description,
        EventLogo=EventLogo,
        GameName=GameName,
        GameLogo=GameLogo,
        Location=Location,
        Time=Time,
        organiser_company=organiser_company,
    )

    # Event_type details (expecting a list of event types)
    event_types_details = request.json.get("EventTypes", [])
    for event_type_detail in event_types_details:
        TierID = event_type_detail.get("TierID")
        Category = event_type_detail.get("Category")
        Price = event_type_detail.get("Price")
        Capacity = event_type_detail.get("Capacity")
        PriceID = event_type_detail.get("PriceID")

        # Create Event_type
        event_type = Event_type(
            TierID=TierID,
            Category=Category,
            Price=Price,
            Capacity=Capacity,
            PriceID=PriceID,
        )

        # Associate Event_type with Event
        event.event_types.append(event_type)

    try:
        db.session.add(event)
        db.session.commit()
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
                "message": "An error occurred while creating the event. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": event.json()
        }
    ), 201

# PUT - edit event's Time or Location
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
        location = request.get_json().get("Location")

        if time != None:
            event.Time = time
        
        if location != None:
            event.Location = location

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

# edit events_type table's capacity 
@app.route("/event_type", methods=['PUT'])
def update_event_type():
    EID = request.get_json().get("EID")
    TierID = request.get_json().get("TierID")  

    try:
        event_type = db.session.scalars(db.select(Event_type).filter_by(EID=EID, TierID=TierID).limit(1)).first()
        if not event_type:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "EID": EID,
                        "TierID": TierID
                    },
                    "message": "event_type not found."
                }
            ), 404

        # Decrement the capacity by 1
        if event_type.Capacity > 0:
            event_type.Capacity -= 1
        else:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "EID": EID,
                        "TierID": TierID
                    },
                    "message": "No more capacity left for this event type."
                }
            ), 400

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": event_type.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "EID": EID,
                    "TierID": TierID
                },
                "message": "An error occurred while updating the event. " + str(e)
            }
        ), 500


# may change port number
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage event ...")
    app.run(host='0.0.0.0', port=5000, debug=True)