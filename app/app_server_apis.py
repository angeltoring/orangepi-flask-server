from flask import request
import os
import json
import requests
headers = {'Content-Type': 'application/json'}
# payload = {
#   'temperature_value': 25.3,
#   'humidity_value': 61,
#   'ppm_value': 690,
#   'ph_value': 6.1,
#   'water_flow_value': 4,
#   'lux_value': 5,
#   'nutsol_reservoir_level': 15,
#   'water_reservoir_Level': 6,
#   'nutrient_a_value': 800,
#   'nutrient_b_value': 9,
#   'ph_up_value': 10,
#   'ph_down_value': 11
# }

def set_variables(payload):
    try:
        # url = os.getenv('API_URL')+f"/update-variables/:{os.getenv('PLANT_ID')}"
        url = "https://nft-hydrophonic-delta.vercel.app/update-variables/1"
        # url = "https://angeltoring-musical-train-x7qx56wg6p4hvxgj-40531.preview.app.github.dev/update-variables/1"
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response)
        return response
    except Exception as e:
        print(f"Error sending data to DB: {e}")

def send_notification(payload):
    try:
        payload["user_id"] = os.getenv("USER_ID")
        url = os.getenv('API_URL')+"/send-specific-notification"
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        return response
    except Exception as e:
        print(f"Error sending notification : {e}")

# set_variables(payload)