from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import json


app = Flask(__name__)
CORS(app)

attendee_URL = "http://attendee:5003/attendee/EID/{EID}"
user_URL = "http://user:5005/user/contact-information"
notification_URL = "http://notification:5010/send-notification"


@app.route("/notification", methods=['POST'])
def create_notification():
    if request.is_json:
        try:
            notification = request.get_json()
            print("\nReceived a notification in JSON:", notification)

            result = getUIDbyEID(notification)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        # need to edit
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "notification.py internal error: " + ex_str
            }), 500
    
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def getUIDbyEID(notification):
    # 2. GET request to get list of uid from eid 
    # Invoke the attendee microservice
    print("\n-----Invoking Attendee microservice-----")

    eid = notification["EID"]

    get_attendeeURL = attendee_URL.format(EID=eid)

    attendee_result = invoke_http(get_attendeeURL, method="GET", json=notification)
    print("attendee_result:", attendee_result)

    # ceck the attendee_result; if a failure, send it to the error microservice
    code = attendee_result["code"]
    if code not in range(200, 300):
        
        invoke_http(notification_URL, method="POST", json=attendee_result)

        return {
            "code": 500,
            "data": {
                "attendee_result": attendee_result
            },
            "message": "Get attendee list failure sent for error handling."
        }
    
    else:
        organised = {
            "EID": eid,
            "notification": notification["notification"],
            "attendee_list":  attendee_result["data"]["attendee_list"],
            "time": notification["time"]
        }

        invoke_user_microservice_result = get_contact_number(organised)

        invoke_http(notification_URL, method="POST", json=invoke_user_microservice_result)

    overall_result = {
        "EID": eid,
        "notification": invoke_user_microservice_result["notification"],
        "time": invoke_user_microservice_result["time"],
        "users": invoke_user_microservice_result["data"]
    }

    return {
        "code": 201,
        "data": {
            "notification": overall_result
        }
    }

def get_contact_number(organised):
    user_results = invoke_http(user_URL, method="GET", json={"attendee_list": organised["attendee_list"]})

    code = user_results['code']
    if code not in range(200,300):

        invoke_http(notification_URL, method="POST", json=user_results)

        return {
            "code": 500,
            "data": {
                "user_results": user_results
            },
            "message": "Get users information failure sent for error handling."
        }
    
    output = organised
    output["users"] = user_results["data"]

    return output
    
# port number
if __name__ == "__main__":
    print("This is flask "+ os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5200, debug=True)
