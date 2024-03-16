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
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db =SQLAlchemy(app)

CORS(app)

# explain why need tierID in events
# shouldnt tierid be foreign key
class Event(db.Model):
    __tablename__ = 'events'
    
    EID = db.Column(db.Integer, primary_key=True)
    TierID = db.Column(db.SmallInteger, primary_key=True)
    GameName = db.Column(db.String(255))
    GameLogo = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    Time = db.Column(db.DateTime)
    GameCompany = db.Column(db.String(255))
    Capacity = db.Column(db.Integer)
    Price = db.Column(db.Float(precision=2))
    
    # Relationships
    attendees = relationship('Attendee', back_populates='event')
    tickets = relationship('Ticket', back_populates='event')

    def __init__(self, EID, TierID, GameName, GameLogo, Location, Time, GameCompany, Capacity, Price):
        self.EID = EID
        self.TierID = TierID
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
            "GameName": self.GameName,
            "GameLogo": self.GameLogo,
            "Location": self.Location,
            "Time": self.Time.isoformat() if self.Time else None,  # ISO formatting for dateTime
            "GameCompany": self.GameCompany,
            "Capacity": self.Capacity,
            "Price": self.Price
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

# POST - create event
@app.route("/event", methods=["POST"])
def create_event():
    EID = request.json.get("EID")
    TierID = request.json.get("TierID")
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
    print()

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
        data = request.get_json()
        if data['Time']:
            event.Time = data['Time']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": event.json()
                }
            ), 200
        
        elif data['Price']:
            event.Price = data['Price']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": event.json()
                }
            ), 200
        
        elif data['Location']:
            event.Location = data['Location']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": event.json()
                }
            ), 200
        
        elif data['Capacity']:
            event.Capacity -= int(data['Capacity'])
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