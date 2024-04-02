from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from invokes import invoke_http


app = Flask(__name__)
CORS(app)

event_URL = "http://event1:5000/event"
ticket_URL = "http://kong:8000/api/v1/ticket"
attendees_list_URL = "http://kong:8000/api/v1/attendee"
update_event_capacity_URL = "http://kong:8000/api/v1/event_type" 


@app.route("/register", methods=["POST"])
def create_attendee_with_ticket():
    # Get JSON data from the POST request
    data = request.get_json()
    EID = data.get("EID")
    UID = data.get("UID")
    TierID = data.get("TierID")
    PriceID = data.get("PriceID")

    # Step 1: Reduce event capacity
    reduce_capacity_response = invoke_http(
        update_event_capacity_URL, method="PUT", json={"EID": EID, "TierID": TierID}
    )
    if reduce_capacity_response["code"] != 200:
        return (
            jsonify(
                {
                    "code": reduce_capacity_response["code"],
                    "message": "Tickets are SOLD OUT!",
                }
            ),
            reduce_capacity_response["code"],
        )

    # Step 2: Create ticket
    create_ticket_response = invoke_http(
        ticket_URL,
        method="POST",
        json={"EID": EID, "TierID": TierID, "PriceID": PriceID, "UID": UID},
    )
    if create_ticket_response["code"] != 201:
        return (
            jsonify(
                {
                    "code": create_ticket_response["code"],
                    "message": "Tickets are SOLD OUT!",
                }
            ),
            create_ticket_response["code"],
        )
    ticket_data = create_ticket_response["data"]["ticket"]

    # Step 3: Create attendee
    create_attendee_response = invoke_http(
        attendees_list_URL,
        method="POST",
        json={"EID": EID, "UID": UID, "ticketID": ticket_data["TicketID"]},
    )
    if create_attendee_response["code"] != 201:
        return (
            jsonify(
                {
                    "code": create_attendee_response["code"],
                    "message": "Failed to create attendee",
                }
            ),
            create_attendee_response["code"],
        )

    return (
        jsonify({"code": 201, "message": "Attendee and ticket created successfully"}),
        201,
    )


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5006, debug=True)
