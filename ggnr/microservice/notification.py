from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

attendee_URL = "http://127.0.0.1:5003/attendee/EID/{EID}"

# exchangename = environ.get("exchangename")
# exchangetype = environ.get("exchangetype")

exchangename = "notification_topic"
exchangetype = "topic"

connection = amqp_connection.create_connection()
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)

@app.route("/notification", methods=['POST'])
def create_notification():
    if request.is_json:
        try:
            notification = request.get_json()
            print("\nReceived a notification in JSON:", notification)

            # 1. 
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
    print(notification["EID"])
    get_attendeeURL = attendee_URL.format(EID=eid)
    print(get_attendeeURL)
    attendee_result = invoke_http(get_attendeeURL, method="GET", json=notification)
    print("attendee_result:", attendee_result)

    # ceck the attendee_result; if a failure, send it to the error microservice
    code = attendee_result["code"]
    message = json.dumps(attendee_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print("\n\n-----Publishing the (attendee error) message with routing_key=attendee.error-----")

        channel.basic_publish(exchange=exchangename, routing_key="attendee.error", 
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(code), attendee_result)

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
        message = json.dumps(organised)
        print('\n\n-----Publishing the notification with routing_key=notification.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        channel.basic_publish(exchange=exchangename, routing_key="notification.info", 
            body=message)
        
    # print("\Notification published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    return {
        "code": 201,
        "data": {
            "notification": organised
        }
    }
    
# port number
if __name__ == "__main__":
    print("This is flask "+ os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)