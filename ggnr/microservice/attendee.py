from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from os import environ
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ggnr_database"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CORS(app)


class Attendee(db.Model):
    __tablename__ = "attendees"

    AID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    EID = db.Column(db.Integer, ForeignKey("events.EID"))
    UID = db.Column(db.Integer, ForeignKey("users.UID"))
    ticketID = db.Column(db.Integer)

    # Relationships
    event = relationship("Event", back_populates="attendees")
    user = relationship("User", back_populates="attendees")

    def __init__(self, EID, UID, ticketID):
        self.EID = EID
        self.UID = UID
        self.ticketID = ticketID

    def json(self):
        return {
            "AID": self.AID,
            "EID": self.EID,
            "UID": self.UID,
            "ticketID": self.ticketID,
        }


class Ticket(db.Model):
    __tablename__ = "tickets"

    TicketID = db.Column(db.Integer, primary_key=True)
    EID = db.Column(db.Integer, ForeignKey("events.EID"))
    TierID = db.Column(db.SmallInteger)
    PriceID = db.Column(db.String(255))

    # Relationships
    event = relationship("Event", back_populates="tickets")
    user_tickets = relationship("UserTicket", back_populates="tickets")

    def __init__(self, TicketID, EID, UID, TierID, PriceID):
        self.TicketID = TicketID
        self.EID = EID
        self.UID = UID
        self.TierID = TierID
        self.PriceID = PriceID

    def json(self):
        return {
            "TicketID": self.TicketID,
            "EID": self.EID,
            "TierID": self.TierID,
            "PriceID": self.PriceID,
        }


class Event(db.Model):
    __tablename__ = "events"

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
    event_types = relationship("Event_type", back_populates="event")
    attendees = relationship("Attendee", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")

    def __init__(
        self,
        Title,
        Description,
        EventLogo,
        GameName,
        GameLogo,
        Location,
        Time,
        organiser_company,
    ):
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
            "Time": (
                self.Time.isoformat() if self.Time else None
            ),  # ISO formatting for dateTime
            "organiser_company": self.organiser_company,
        }


class Event_type(db.Model):
    __tablename__ = "events_type"

    EID = db.Column(db.Integer, db.ForeignKey("events.EID"), primary_key=True)
    TierID = db.Column(db.SmallInteger, primary_key=True)
    Category = db.Column(db.String(255))
    Capacity = db.Column(db.Integer)
    Price = db.Column(db.Float)
    PriceID = db.Column(db.String(255))

    # Relationships
    event = relationship("Event", back_populates="event_types")

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
    __tablename__ = "users"

    UID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferences = db.Column(db.Text)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    organiser = db.Column(db.Boolean, nullable=False)
    organiser_company = db.Column(db.String(255))

    # Relationships
    attendees = relationship("Attendee", back_populates="user")
    user_tickets = relationship("UserTicket", back_populates="user")

    def __init__(
        self,
        username,
        password_hash,
        preferences,
        email,
        contact,
        organiser,
        organiser_company,
    ):
        self.username = username
        self.password_hash = password_hash
        self.preferences = preferences
        self.email = email
        self.contact = contact
        self.organiser = organiser
        self.organiser_company = organiser_company

    def json(self):
        return {
            "UID": self.UID,
            "username": self.username,
            "preferences": self.preferences,
            "email": self.email,
            "contact": self.contact,
            "organiser": self.organiser,
            "organiser_company": self.organiser_company,
        }


class UserTicket(db.Model):
    __tablename__ = "user_tickets"

    UID = db.Column(db.Integer, ForeignKey("users.UID"), primary_key=True)
    TicketID = db.Column(db.Integer, ForeignKey("tickets.TicketID"), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="user_tickets")
    tickets = relationship("Ticket", back_populates="user_tickets")

    def __init__(self, UID, TicketID):
        self.UID = UID
        self.TicketID = TicketID

    def json(self):
        return {"UID": self.UID, "TicketID": self.TicketID}


@app.route("/attendee")
def get_all():
    # get all attendees
    attendeelist = db.session.scalars(db.select(Attendee)).all()
    if len(attendeelist):
        return jsonify(
            {
                "code": 200,
                "data": {"attendees": [attendee.json() for attendee in attendeelist]},
            }
        )

    return jsonify({"code": 404, "message": "There are no attendees."}), 404


# Get by EID
@app.route("/attendee/EID/<string:EID>")
def get_attendee_by_EID(EID):
    # get all attendees by EID
    attendee_list = db.session.scalars(db.select(Attendee).filter_by(EID=EID)).all()

    if len(attendee_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "attendee_list": [attendee.json() for attendee in attendee_list]
                },
            }
        )

    return jsonify({"code": 404, "message": "There are no attendees."}), 404


# Get by UID
@app.route("/attendee/UID/<string:UID>")
def get_attendee_by_UID(UID):
    # get all attendees by UID
    attendee_list = db.session.scalars(db.select(Attendee).filter_by(UID=UID)).all()

    if len(attendee_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "attendee_list": [attendee.json() for attendee in attendee_list]
                },
            }
        )

    return jsonify({"code": 404, "message": "There are no attendees."}), 404


# POST - create attendee
@app.route("/attendee", methods=["POST"])
def create_attendee():
    # Create an attendee
    EID = request.json.get("EID")
    uid = request.json.get("UID")
    ticketID = request.json.get("ticketID")

    attendee = Attendee(EID, uid, ticketID)

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

        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred creating the attendee. " + ex_str,
                }
            ),
            500,
        )

    return jsonify({"code": 201, "data": attendee.json()}), 201


@app.route("/attendee/<string:EID>", methods=["DELETE"])
def delete_attendee_list(EID):
    # Delete all attendees by EID
    attendee_list = db.session.scalars(db.select(Attendee).filter_by(EID=EID)).all()

    if len(attendee_list):
        for attendee in attendee_list:
            try:
                db.session.delete(attendee)
                db.session.commit()
                return {"code": 201, "message": "Event attendee list has been deleted."}
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

                return (
                    jsonify(
                        {
                            "code": 500,
                            "data": {"EID": EID},
                            "message": "An unexpected error occurred deleting the attendee list. "
                            + ex_str,
                        }
                    ),
                    500,
                )

    return (
        jsonify(
            {"code": 404, "data": {"EID": EID}, "message": "Attendee list not found."}
        ),
        400,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
