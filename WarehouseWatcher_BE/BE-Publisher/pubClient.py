# FILE : pubClient.py
# PROGRAMMER : Yujung Park
# DESCRIPTION : pubClient.py connects to the host, creates a random value between 24 and 30 and makes the mock thermostat temperature message and publishes the message on the topic.
# https://github.com/eclipse-paho/paho.mqtt.python

import paho.mqtt.client as paho
import time
import random
from paho.mqtt.enums import CallbackAPIVersion
import configparser
from Sensors.thermostat import thermostat

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DEFAULT', 'UserName')
password = config.get('DEFAULT', 'Password')
host = config.get('DEFAULT', 'Host')

TOPICS={
    "Room":"Room:Waterloo/Warehouse/Thermostat1/temperature"
}

thermostats = {
    "Room": thermostat("Room", (16.0, 25.0), battery_drain_cycle=100),  # Drains in 100 cycles
    
}
try:
    while True:
        print(thermostat("Room", (16.0, 25.0), battery_drain_cycle=100))
        time.sleep(3)
except KeyboardInterrupt:
    print("Stopped by user")
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

def publish_sensorData(client):
    for sensor,topic in list(TOPICS.item()):
        load=thermostat[sensor].generate_sensor_data()
        if load is None:
            print(f"{sensor} sensor battery is dead.Stopping")
            del TOPICS[sensor]
            continue
        (rc,mid)=client.publish(TOPICS,load,qos=1)
        print(f"Publishing: {topic}:{load}(mid :{mid}, rc:{rc})")
try:
    while True:
        temperature = round(random.uniform(24, 30), 1)
        (rc, mid) = client.publish('Kitchener/Office1/Thermostat1/temperature', str(temperature), qos=1)
       
        time.sleep(3)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()  # Stop the network loop
    client.disconnect()  # Disconnect the client
