from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

from invokes import invoke_http

from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)

event_URL = "http://kong:8000/check_events_in_the_next_hour" # may need to edit the url
attendee_URL = "http://kong:8000/attendee/{EID}"
user_URL = "http://kong:8000/user/contact-information"
notification_URL = "http://kong:8000/api/v1/create_notification"


@app.route("/custom_notification", methods=["POST"])
def create_notification():
    # Get  JSON data from the POST request
    if request.is_json:
        try:
            notification = request.get_json()
            print("\nReceived a notification in JSON:", notification)

            result = getUIDbyEID(notification)
            print("\n------------------------")
            print("\nresult: ", result)
            return jsonify(result), result["code"]

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

            return (
                jsonify(
                    {
                        "code": 500,
                        "message": "notification.py internal error: " + ex_str,
                    }
                ),
                500,
            )

    # if reached here, not a JSON request.
    return (
        jsonify(
            {"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}
        ),
        400,
    )


def getUIDbyEID(notification):
    # 2. GET request to get list of uid from eid
    # Invoke the attendee microservice
    print("\n-----Invoking Attendee microservice-----")

    eid = notification["EID"]

    get_attendeeURL = attendee_URL.format(EID=eid)
    attendee_result = invoke_http(get_attendeeURL, method="GET", json=notification)
    print("attendee_result:", attendee_result)

    # check the attendee_result; if a failure, send it to the error microservice
    code = attendee_result["code"]
    if code not in range(200, 300):

        invoke_http(notification_URL, method="POST", json=attendee_result)

        return {
            "code": 500,
            "data": {"attendee_result": attendee_result},
            "message": "Get attendee list failure sent for error handling.",
        }

    else:
        organised = {
            "EID": eid,
            "notification": notification["notification"],
            "attendee_list": attendee_result["data"]["attendee_list"],
            "time": notification["time"],
            "code": 201,
        }

        invoke_user_microservice_result = get_contact_number(organised)

    overall_result = {
        "EID": eid,
        "notification": organised["notification"],
        "time": organised["time"],
        "users": {"data": invoke_user_microservice_result["users"]},
        "code": 201,
    }
    print("overall results", overall_result)
    invoke_http(notification_URL, method="POST", json=overall_result)

    return {"code": 201, "data": {"notification": overall_result}}


def get_contact_number(organised):
    user_results = invoke_http(
        user_URL, method="GET", json={"attendee_list": organised["attendee_list"]}
    )
    code = user_results["code"]
    if code not in range(200, 300):

        invoke_http(notification_URL, method="POST", json=user_results)

        return {
            "code": 500,
            "data": {"user_results": user_results},
            "message": "Get users information failure sent for error handling.",
        }

    output = organised
    output["users"] = user_results.get("data")

    return output


# scenario 3
@app.route("/schedule_notification", methods=["GET"])
def schedule_notification():
    # 1. GET request to get list of events happening in the next hour

    event_results = invoke_http(event_URL, method="GET", json={})
    print("\n------------------------")
    print("\nresult: ", event_results)

    if event_results["code"] not in range(200, 300):
        return {
            "code": 500,
            "data": {"event_results": event_results},
            "message": "There are no events happening in 1 hour.",
        }

    event_list = event_results["data"]["events"]

    all_events_without_attendees = True  # flag to check if all events have no attendees

    for event in event_list:

        # invoke attendee microservice
        print("\n-----Invoking Attendee microservice-----")
        eid = event["EID"]
        get_attendeeURL = attendee_URL.format(EID=eid)
        attendee_results = invoke_http(get_attendeeURL, method="GET", json={})
        print(attendee_results)

        if attendee_results["code"] in range(200, 300):

            print("attendee_result:", attendee_results)

            # invoke users microservice
            print("\n-----Invoking Users microservice-----")
            user_results = invoke_http(
                user_URL,
                method="GET",
                json={"attendee_list": attendee_results["data"]["attendee_list"]},
            )
            print("user_results", user_results)
            code = user_results["code"]

            if code in range(200, 300):
                # invoke notification microserivce - send notification
                print("\n-----Invoking Notification microservice-----")
                event_title = event.get("Title", "")
                game_company = event.get("GameCompany", "")
                event_location = event.get("Location", "")
                event_time = event.get("Time", "")
                time_obj = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S")
                time_am_pm = time_obj.strftime("%I:%M %p")

                thrity_mins_before = time_obj - timedelta(minutes=58)
                event_time_format = thrity_mins_before.strftime("%Y-%m-%dT%H:%M:%S")

                message = f"Hello gamers! Thank you for signing up for {event_title} organised by {game_company}. The event will start in about 1 hour at {time_am_pm} and will take place at {event_location}. Do not be late and see you there!"

                organised = {
                    "code": 201,
                    "users": user_results,
                    "time": event_time_format,
                    "notification": message,
                }

                result = invoke_http(notification_URL, method="POST", json=organised)
                all_events_without_attendees = False  # unflag the flag

    if all_events_without_attendees:
        # flag is still true, no attendees in all events
        return (
            jsonify({"code": 404, "message": "There are no notifications sent."}),
            404,
        )

    return (
        jsonify(
            {
                "code": 201,
                "message": "Notifications have been sent to the users.",
                "data": result,
            }
        ),
        201,
    )


# port number
if __name__ == "__main__":
    print(
        "This is flask "
        + os.path.basename(__file__)
        + " for sending scheduled notifications..."
    )
    app.run(host="0.0.0.0", port=5200, debug=True)
