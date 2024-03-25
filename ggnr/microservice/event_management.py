from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
import json

app = Flask(__name__)
CORS(app)

# URLs of other microservices
events_url = "http://127.0.0.1:5000/create_event"

@app.route("/create_event", methods=["POST"])
def create_event():
    # Extract event data from the request
    event_data = request.get_json()

    try:
        response = invoke_http(events_url, method='POST', json=event_data)
        if response["code"] not in range(200, 300):
            # Handle the error appropriately
            print("Error sending event data to other service:", response)
            return jsonify({"code": 500, "message": "Failed to send event data to the other service."}), 500
    except Exception as e:
        print("An error occurred while sending the event data:", e)
        return jsonify({"code": 500, "message": "Internal server error"}), 500

    # Return a success response
    return jsonify({"code": 201, "message": "Event created successfully"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
