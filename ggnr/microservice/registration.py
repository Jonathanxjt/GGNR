from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os, sys
from os import environ
import requests
from invokes import invoke_http
import json
import random
import string

app = Flask(__name__)
CORS(app)

# URLs of other microservices
# always follow service names in YAML, e.g. http://event:5000 for event microservice
#* http://<service_name>:<port_number>/<endpoint>   FOLLOW THIS!!!

event_URL = "http://event:5000/event"
ticket_URL = "http://ticket:5008/ticket"
attendees_list_URL = "http://attendee:5003/attendee"
update_event_capacity_URL = "http://event:5000/event_type" 
# need to use different ports because all of them are running on localhost, if not there will be a port conflict
# can use same port if they are all running on different machines(?) basically not all using localhost

# ? May remove, not sure as database is in a mess right now 
def generate_transaction_id(length=8):
    return ''.join(random.choices(string.digits, k=length))

@app.route("/register", methods=["POST"])
def create_attendee_with_ticket():
    data = request.get_json()
    EID = data.get("EID")
    UID = data.get("UID")
    TierID = data.get("TierID")
    PriceID = data.get("PriceID")
    transactionID = generate_transaction_id()

    # Step 1: Reduce event capacity
    reduce_capacity_response = invoke_http(update_event_capacity_URL, method='PUT', json={"EID": EID, "TierID": TierID})
    if reduce_capacity_response["code"] != 200:
        return jsonify({"code": reduce_capacity_response["code"], "message": "Failed to reduce event capacity"}), reduce_capacity_response["code"]

    # Step 2: Create ticket
    create_ticket_response = invoke_http(ticket_URL, method='POST', json={"EID": EID, "TierID": TierID, "PriceID": PriceID, "UID": UID})
    if create_ticket_response["code"] != 201:
        return jsonify({"code": create_ticket_response["code"], "message": "Failed to create ticket"}), create_ticket_response["code"]
    ticket_data = create_ticket_response["data"]["ticket"]

    # Step 3: Create attendee
    create_attendee_response = invoke_http(attendees_list_URL, method='POST', json={"EID": EID, "UID": UID, "ticketID": ticket_data["TicketID"], "transactionID": transactionID})
    if create_attendee_response["code"] != 201:
        return jsonify({"code": create_attendee_response["code"], "message": "Failed to create attendee"}), create_attendee_response["code"]

    return jsonify({"code": 201, "message": "Attendee and ticket created successfully"}), 201

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5006, debug=True)