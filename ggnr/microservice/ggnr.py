from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/ggnr_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    Price = db.Column(db.Float)
    
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
            "Time": self.Time.isoformat() if self.Time else None,  # ISO formatting for datetime
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
    def __init__(self, EID, UID, Tier, Price):
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)