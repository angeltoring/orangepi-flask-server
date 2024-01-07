import serial
import threading
from .app_server_apis import set_variables, send_notification
from .codes import send_codes, receive_codes
import paho.mqtt.client as mqtt
import time
from .object_detection import capture_and_send_frame
import requests
import os

# Open the serial connection.
# In Ubuntu or any other Linux-based system, the Arduino board usually connects to the serial port named like /dev/ttyACM0 or /dev/ttyUSB0. 
# The exact name can vary based on your specific system configuration.
# You can list all the available serial ports using the command ls /dev/tty* in the terminal. 
# This command will list all tty devices.
# If you have multiple devices and you want to find out which one is the Arduino, 
# you can observe the change in output of ls /dev/tty* command before and after plugging the Arduino board.
# Another way to get the name of the serial port for Arduino is using the Arduino IDE itself.
# When you connect your Arduino board, go to Tools > Port in the Arduino IDE. The IDE will list the port to which Arduino is connected. 

#***uncomment this below line****
# ser = serial.Serial('/dev/ttyACM0', 9600)

def send_data(command):
    i = 0
    while i < 1:
        try:
            #*********** uncomment this below line*************
            # ser.write(command.encode()) 
            print("Command sent to arduino: ", command)
            i += 1
        except Exception as e:
            print(f"Error sending data to Arduino: {e}")

def receive_data_from_arduino():
    time.sleep(2)
    # while True:  # Loop indefinitely
    # while (ser.inWaiting() == 0):
    #     pass
    try:
        #*********** uncomment this below line*************
        # data = ser.readline().decode().strip()/
        data=''
        if len(data)!=0:
            print("Command received from arduino: ", data)
            if len(data) == 1:
                send_notification({
                    'notification_type' : receive_codes[data]
                })
            else:
                temp = data.split(',')
                if len(temp) > 1:
                    if len(temp)!=12:
                        print(f"Unknown command received from Arduino: {data}")
                    else :
                        payload = {
                            'temperature_value': float(temp[0]),
                            'humidity_value': int(temp[1]),
                            'ppm_value': int(temp[2]),
                            'ph_value': float(temp[3]),
                            'water_flow_value': int(temp[4]),
                            'lux_value': int(temp[5]),
                            'nutsol_reservoir_level': int(temp[6]),
                            'water_reservoir_Level': int(temp[7]),
                            'nutrient_a_value': int(temp[8]),
                            'nutrient_b_value': int(temp[9]),
                            'ph_up_value': int(temp[10]),
                            'ph_down_value': int(temp[11])
                        }
                        set_variables(payload)
    except Exception as e :
        print(f"Error receiving data from Arduino: {e}")
                
def start_serial_comm():
    receive_thread = threading.Thread(target=receive_data_from_arduino)
    detection_thread = threading.Thread(target=capture_and_send_frame)
 
    receive_thread.start()
    detection_thread.start()

    receive_thread.join()
    detection_thread.join()

# Cloud server details
check_interval = 1.5  # Check every 5 seconds (adjust as needed)
def check_for_events():
    url = '/check-code'

    response = requests.get(os.getenv('API_URL') + url)
    response.raise_for_status()
    data = response.json()

    if len(data['data']) == 1:
        try:
            # Process the received events as needed
            print('Response from server:', data)
            send_data(data['data'])
        except requests.exceptions.RequestException as e:
            print('Error decoding JSON:', e)


def command_from_app():   
    # Set up an interval to periodically check for new events
    while True:
        check_for_events()
        time.sleep(check_interval)    

start_serial_comm()  
command_from_app()
# client = mqtt.Client()
# client.username_pw_set("dqjzgogh", "bhZjcIOCcqWP")  # replace with your CloudMQTT username and password

# def on_message(client, userdata, msg):
#     command = msg.payload.decode()
#     print(command)
#     send_data(command)

# client.on_message = on_message
# client.connect("driver.cloudmqtt.com", 18915)  # replace with your CloudMQTT server and port
# client.subscribe("commands")

# def start_mqtt_client():
#     try:
#         client.loop_start()
#     except Exception as e:
#         print(f"Error starting MQTT client: {e}")

# start_mqtt_client()
