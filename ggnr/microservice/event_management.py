from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
from os import environ
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


events_url = "http://kong:8000/event/create_event"
user_url = "http://kong:8000/user/user_preference_gamename"
search_url = "http://kong:8000/search"
notification_url = "http://kong:8000/api/v1/create_notification"


# Search for games:
@app.route("/search", methods=["POST"])
def search_games():
    game_name = request.json.get("game_name")
    search_results = invoke_http(
        search_url, method="POST", json={"game_name": game_name}
    )
    return jsonify(search_results)


# Creating an event
@app.route("/create", methods=["POST"])
def create_event():
    # Extract event data from the request
    if request.is_json:
        try:
            event_data = request.get_json()
            event_response = invoke_event_microservice(event_data)
            game_name = event_data.get("GameName", "")
            user_data = {"GameName": game_name}
            user_response = invoke_user_microservice(user_data)

            if user_response["data"] == []:
                # Event created but no users to notify
                return (
                    jsonify(
                        {
                            "code": 201,
                            "message": "Event created successfully, but no users to notify.",
                        }
                    ),
                    201,
                )

            else:
                # get params from event_data
                event_title = event_data.get("Title", "")
                event_time = event_data.get("Time", "")
                time_obj = datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S")
                time_am_pm = time_obj.strftime("%I:%M %p")
                game_company = event_data.get("GameCompany", "")
                event_location = event_data.get("Location", "")

                message = f"Hello gamers! We are excited to announce a brand-new event: {event_title}, organized by {game_company}! The event will be focused on {game_name} and will be held at {event_location}, {time_am_pm}. This is a good opportunity you won't want to miss. Sign up now on GGNR!"
                current_time_plus_3min = datetime.now() + timedelta(minutes=2)
                current_time_plus_3min_str = current_time_plus_3min.strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )
                organised = {
                    "notification": message,
                    "users": user_response,
                    "time": current_time_plus_3min_str,
                    "code": 201,
                }
                # send message to the notification queue
                result = invoke_http(notification_url, method="POST", json=organised)
                return (
                    jsonify(
                        {
                            "code": 201,
                            "message": "Event created successfully, notifications sent.",
                            "data": result,
                        }
                    ),
                    201,
                )
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = (
                str(e)
                + " at "
                + str(exc_type)
                + ": "
                + fname
                + ": line "
                + str(exc_tb.tb_lineno)
            )
            print(ex_str)
            return jsonify({"code": 500, "message": "Internal server error"}), 500

    # if reached here, not a JSON request.
    return (
        jsonify(
            {"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}
        ),
        400,
    )


def invoke_event_microservice(event_data):
    try:
        # Invoke the event microservice
        response = invoke_http(events_url, method="POST", json=event_data)
        if response["code"] not in range(200, 300):
            # Handle the error appropriately
            print("Error sending event data to other service:", response)

            invoke_http(notification_url, method="POST", json=response)

            return (
                jsonify(
                    {
                        "code": 500,
                        "message": "Failed to send event data to the other service.",
                    }
                ),
                500,
            )

    except Exception as e:
        # Handle exceptions
        print("Error invoking event microservice:", e)

        invoke_http(
            notification_url,
            method="POST",
            json={"code": 500, "message": "Internal server error"},
        )

        return (
            jsonify(
                {
                    "code": 500,
                    "message": "Failed to send event data to the other service.",
                }
            ),
            500,
        )

    return jsonify({"code": 201, "message": "Event created successfully"}), 201


def invoke_user_microservice(data):

    print("\n-----Invoking User microservice-----")
    user_result = invoke_http(user_url, method="GET", json=data)
    code = user_result["code"]

    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"user_result": user_result},
            "message": "Get user list failed.",
        }

    return user_result


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for creating an event...")
    app.run(host="0.0.0.0", port=5100, debug=True)
