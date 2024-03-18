from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

event_URL = "http://localhost:5000/event"
ticket_URL = "http://localhost:5008/ticket"
attendees_list_URL = "http://localhost:5003/attendee"
error_URL = "http://localhost:5007/error"   
update_event_URL = "http://localhost:5000/event/{EID}" 
create_ticket_URL = "http://localhost:5008/ticket/{TID}"
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
    price = order_result["data"]["Price"]
    print("\nTicket sent to events.\n")


    # 3. Create the ticket 
    # Invoke the ticket microservice
    print('\n-----Invoking ticket microservice-----')
    tid = order["TID"]
    created_ticket_url = create_ticket_URL.format(TID=tid,Price=price)
    ticket_created = invoke_http(created_ticket_url, method="POST", json=order)
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

    # Inform the error microservice
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=order_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Order status ({:d}) sent to the error microservice:".format(code), order_result)

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