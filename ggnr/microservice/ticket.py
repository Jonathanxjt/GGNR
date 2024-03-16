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

db = SQLAlchemy(app)

CORS(app)

class Ticket(db.Model):
    __tablename__ = "ticket"

    TicketID = db.Column(db.Integer, primary_key=True)
    EID = db.Column(db.Integer, ForeignKey('events.EID'))
    UID = db.Column(db.Integer, ForeignKey('users.UID'))
    Tier = db.Column(db.SmallInteger)
    Price = db.Column(db.Float)
    
    # Relationships
    event = relationship('Event', back_populates='tickets')
    user = relationship('User', back_populates='tickets')
    def __init__(self, EID, UID, Tier, Price):
        self.EID = EID
        self.UID = UID
        self.Tier = Tier
        self.Price = Price
    
    def to_json(self):
        return {
            'TicketID': self.TicketID,
            'EID': self.EID,
            'UID': self.UID,
            'Tier': self.Tier,
            'Price': self.Price
        }
    

@app.route("/ticket")
def get_all():

    
    eid = request.args.get("EID")
    uid = request.args.get("UID")

    # get ticket by eid and uid
    if eid != None and uid != None:
        ticket = db.session.scalars(db.select(Ticket).filter_by(EID=eid).filter_by(UID=uid).limit(1)).first()

        if ticket:
            return jsonify(
                {
                    "code": 200,
                    "data": ticket.json()
                }
            )
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Ticket not found."
                }
            ), 404
        
    if eid != None:
        ticket_list_by_eid = db.session.scalars(db.select(Ticket).filter_by(EID=eid)).all()
        
        if len(ticket_list_by_eid):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "tickets": [individual_ticket.json() for individual_ticket in ticket_list_by_eid]
                    }
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no tickets."
                }
            ), 404
    
    if uid != None:
        ticket_list_by_uid = db.session.scalars(db.select(Ticket).filter_by(UID=uid)).all()

        if len(ticket_list_by_uid):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "tickets": [individual_ticket.json() for individual_ticket in ticket_list_by_uid]
                    }
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "There are no tickets."
                }
            ), 404

    ticket_list = db.session.scalars(db.select(Ticket)).all()
    if len(ticket_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tickets": [ticket.json() for ticket in ticket_list]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no tickets."
        }
    ), 404


# POST - create ticket
@app.route("/ticket/<string:TicketID>", methods=["POST"])
def create_ticket(TicketID):

    eid = request.args.get("EID")
    uid = request.args.get("UID")
    tier = request.args.get("Tier")
    price = request.args.get("Price")

    ticket = Ticket(
        TicketID = TicketID,
        EID = eid,
        UID = uid,
        Tier = tier,
        Price = price
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
    
    print(json.dumps(ticket.json()), default=str)
    print()

    return jsonify(
        {
            "code": 201,
            "data": ticket.json()
        }
    ), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)