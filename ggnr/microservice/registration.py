from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os, sys
from os import environ
import requests
from invokes import invoke_http
import json
app = Flask(__name__)
CORS(app)


# URLs of other microservices
# always follow service names in YAML, e.g. http://event:5000 for event microservice
#* http://<service_name>:<port_number>/<endpoint>   FOLLOW THIS!!!
event_URL = "http://event:5000/event"
ticket_URL = "http://ticket:5008/userticket"
attendees_list_URL = "http://attendee:5003/attendee"
update_event_URL = "http://event:5000/event/{EID}" 
# need to use different ports because all of them are running on localhost, if not there will be a port conflict
# can use same port if they are all running on different machines(?) basically not all using localhost

@app.route("/registration", methods=["GET"])
def registration():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {ticket}
            result = processBuyTicket(order)
            print(result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "registration.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processBuyTicket(order):
    # 2. PUT request to reduce capacity of Events
    print('\n\n-----Invoking events microservice-----')
    eid = order['EID']  # Assuming 'EID' is a key in the 'order' dictionary
    updated_event_url = update_event_URL.format(EID=eid)
    order_result = invoke_http(updated_event_url, method="PUT", json=order)
    print(order_result)
    print("\nTicket sent to events.\n")


    # 3. Create the ticket 
    # Invoke the ticket microservice
    print('\n-----Invoking ticket microservice-----')
    ticket_created = invoke_http(ticket_URL, method="POST", json=order)
    print('Created_Ticket:', ticket_created)

    # 4. Record in attendee_list microservice
    print('\n\n-----Invoking attendee_list microservice-----')
    invoke_http(attendees_list_URL, method="GET", json=order_result)
    print("\nAttendees list updated\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    # Check the order result; if a failure, send it to the error microservice.
    code = order_result["code"]
    if code not in range(200, 300):

    # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure sent for error handling."
        }
    return order_result
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5006, debug=True)