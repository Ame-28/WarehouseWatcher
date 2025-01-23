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
import json

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

user = config.get('DEFAULT', 'UserName')
password = config.get('DEFAULT', 'Password')
host = config.get('DEFAULT', 'Host')

TOPICS={
    "temperature": "Waterloo/Warehouse/{sensor_name}/temperature",
    "voltage": "Waterloo/Warehouse/{sensor_name}/voltage",
    "battery": "Waterloo/Warehouse/{sensor_name}/battery",
    "signal_strength": "Waterloo/Warehouse/{sensor_name}/signal_strength",
    # "everydata":"Waterloo/Warehouse/{sensor_name}"
}

thermostats = {
     "Room": thermostat("Room", (20.0, 25.0), battery_drain_cycle=100),
    "Refrigerator": thermostat("Refrigerator", (2.0, 5.0), battery_drain_cycle=150),
    "Freezer": thermostat("Freezer", (-18.0, -15.0), battery_drain_cycle=200),
}

# Publish, print the message on the console
def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message published. MID: {mid}, Reason Code: {reason_code}")


def publish_sensorData(client):
    key_mapping = {
        "temperature": "Data",
        "voltage": "Voltage",
        "battery": "Battery",
        "signal_strength": "SignalStrength",
        # "everydata":"Result"
    }

    for sensor_name, thermostat_instance in thermostats.items():
        data = thermostat_instance.generate_sensor_data()
        if data is None:
            print(f"{sensor_name} has shut down.")
            continue

        result = json.loads(data)["Result"][0]
        for key, topic_template in TOPICS.items():
            topic = topic_template.format(sensor_name=sensor_name)
            mapped_key = key_mapping[key] 
            payload = result[mapped_key]
            client.publish(topic, payload, qos=1)
            print(f"Published to {topic}: {payload}")


if __name__ == "__main__":
    client = paho.Client(callback_api_version= CallbackAPIVersion.VERSION2, client_id="", clean_session=True)
    client.tls_set() 
    client.username_pw_set(user, password)

    client.on_publish = on_publish
    client.connect(host, 8883)
    client.loop_start()
    try:
        while TOPICS:
            publish_sensorData(client)
            time.sleep(3)
    except KeyboardInterrupt:
     print("Exiting...")
    finally:
     client.loop_stop()  
     client.disconnect()  # Disconnect the client

