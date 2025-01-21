# FILE : pubClient.py
# PROGRAMMER : Yujung Park
# DESCRIPTION : pubClient.py connects to the host, creates a random value between 24 and 30 and makes the mock thermostat temperature message and publishes the message on the topic.
# https://github.com/eclipse-paho/paho.mqtt.python

import paho.mqtt.client as paho
import time
import random
from paho.mqtt.enums import CallbackAPIVersion
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DEFAULT', 'UserName')
password = config.get('DEFAULT', 'Password')
host = config.get('DEFAULT', 'Host')

# Publish, print the message on the console
def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message published. MID: {mid}, Reason Code: {reason_code}")
client = paho.Client(callback_api_version= CallbackAPIVersion.VERSION2, client_id="", clean_session=True)

# Enable TLS/SSL
client.tls_set() 
client.username_pw_set(user, password)

client.on_publish = on_publish
client.connect(host, 8883)
client.loop_start()

try:
    while True:
        temperature = round(random.uniform(24, 30), 1)
        (rc, mid) = client.publish('Kitchener/Office1/Thermostat1/temperature', str(temperature), qos=1)
        print(f"Publishing: {temperature} with mid: {mid} (rc: {rc})")  # Added print statement
        time.sleep(3)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()  # Stop the network loop
    client.disconnect()  # Disconnect the client
