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

# what is AID
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
    
    def to_json(self):
        return {
            'AID': self.AID,
            'EID': self.EID,
            'UID': self.UID,
            'ticketID': self.ticketID,
            'transactionID': self.transactionID
        }
    

# Get all
@app.route("/attendee")
def get_all():
    attendeelist = db.session.scalars(db.select(Attendee)).all()
    if len(attendeelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "attendees": [attendee.json() for attendee in attendeelist]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no attendees."
        }
    ), 404


# Get by EID
@app.route("/attendee/EID/<string:EID>")
def get_attendee_by_EID(EID):
    attendee_list = db.session.scalars(db.select(Attendee).filter_by(EID=EID)).all()

    if len(attendee_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "attendee_list": [attendee.json() for attendee in attendee_list]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no attendees."
        }
    ), 404


# Get by UID
@app.route("/attendee/UID/<string:UID>")
def get_attendee_by_UID(UID):
    attendee_list = db.session.scalrs(db.select(Attendee).filter_by(UID=UID)).all()

    if len(attendee_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "attendee_list": [attendee.json() for attendee in attendee_list]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no attendees."
        }
    ), 404

# POST - create attendee
@app.route("/attendee", methods=["POST"])
def create_attendee():
    EID = request.json.get("EID")
    uid = request.json.get("UID")
    ticketID = request.json.get("ticketID")
    transactionID = request.json.get("transactionID")

    attendee = Attendee(EID, uid, ticketID, transactionID)

    try:
        db.session.add(attendee)
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
                "message": "An error occurred creating the attendee. " + ex_str,
            }
        ), 500
    
    # print(json.dumps(attendee.json(), default=str)) # convert a JSON object to a string and print
    # print()

    return jsonify(
        {
            "code": 201,
            "data": attendee.json()
        }
    ), 201

@app.route("/attendee/<string:EID>", methods=["DELETE"])
def delete_attendee_list(EID):
    attendee_list = db.session.scalars(db.select(Attendee).filter_by(EID=EID)).all()

    if len(attendee_list):
        for attendee in attendee_list:
            try:
                db.session.delete(attendee)
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
                        "message": "An unexpected error occurred deleting the attendee list. " + ex_str,
                    }
                ), 500 

    return jsonify(
            {
                "code": 404, 
                "data": {"EID": EID}, 
                "message": "Attendee list not found."
            }
        ), 400


# change port?
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)