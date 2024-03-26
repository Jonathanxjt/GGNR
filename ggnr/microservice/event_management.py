from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
import json

app = Flask(__name__)
CORS(app)

# URLs of other microservices
events_url = "http://127.0.0.1:5000/event/create_event"
user_url = "http://127.0.0.1:5005/user/perference"
notification_url = "http://127.0.0.1:5200/notification"

@app.route("/create", methods=["POST"])
def create_event():
    if request.is_json:
        
        try:
            # Extract event data from the request
            event_data = request.get_json()
            event_response = invoke_event_microservice(event_data)

            game_name = event_response["data"]["GameName"]
            user_data = {"GameName": game_name}
            user_response = invoke_user_microservice(user_data)

            # notification.py - need to create new function since data different
            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            return jsonify({"code": 500, "message": "Internal server error"}), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def invoke_event_microservice(event_data):

    print("\n-----Invoking Event microservice-----")
    event_result = invoke_http(events_url, method="POST", json=event_data)
    code = event_result["code"]

    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {
                "event_result": event_result
            },
            "message": "Creation of events failed."
        }
    
    return event_result

def invoke_user_microservice(data):

    print("\n-----Invoking User microservice-----")
    user_result = invoke_http(user_url, method="GET", json=data)
    code = user_result["code"]

    if code not in range(200,300):
        return {
            "code": 500,
            "data": {
                "user_result": user_result
            },
            "message": "Get user list failed."
        }
    
    return user_result

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
