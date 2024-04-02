import requests
import time

url = "http://custom_notification:5200/schedule_notification"


try:
    response = requests.get(url)
    print(f"Request to {url} succeeded with status code {response.status_code}.")
    time.sleep(60)

except requests.exceptions.RequestException as e:
    print(f"Request to {url} failed: {e}")
