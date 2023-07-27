from flask import Flask
import os
from .arduino import start_serial_comm, start_mqtt_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    try:
        # Set up and start the serial communication thread
        start_serial_comm()
    except Exception as e:
        print(f"Error starting serial communication: {e}")

    try:
        # Start the MQTT client
        start_mqtt_client()
    except Exception as e:
        print(f"Error starting MQTT client: {e}")

    # more app setup code here

    return app
