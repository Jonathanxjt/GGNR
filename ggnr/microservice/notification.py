from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import json
import pika
import amqp_connection

app = Flask(__name__)
CORS(app)

# get the environment variables
exchangename = environ.get("exchangename")
exchangetype = environ.get("exchangetype")

connection = amqp_connection.create_connection()
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print(
        "\nCreate the 'Exchange' before running this microservice. \nExiting the program."
    )
    sys.exit(0)


@app.route("/send-notification", methods=["POST"])
def send_notification():
    # Get JSON data from the POST request
    if request.is_json:
        response = request.get_json()
        print(response)
        if response["code"] not in range(200, 300):
            print(
                "\n\n-----Publishing the (notification error) message with routing_key=*.error-----"
            )
            message = json.dumps(response)
            channel.basic_publish(
                # publish the message to the exchange
                exchange=exchangename,
                routing_key="notification.error",
                body=message,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            return jsonify({"code": 500, "message": "There is an error."})

        else:
            print(
                "\n\n-----Publishing the (notification info) message with routing_key=*.info-----"
            )
            message = json.dumps(response)
            channel.basic_publish(
                # publish the message to the exchange
                exchange=exchangename,
                routing_key="notification.info",
                body=message,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            return jsonify({"code": 201, "message": "Message has been sent."})

    else:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "Invalid JSON input: " + str(request.get_data()),
                }
            ),
            400,
        )


if __name__ == "__main__":
    print(
        "This is flask " + os.path.basename(__file__) + " for sending notification..."
    )
    app.run(host="0.0.0.0", port=5010, debug=True)
