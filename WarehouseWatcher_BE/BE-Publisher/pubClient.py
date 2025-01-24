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
from dotenv import load_dotenv

import os
 

load_dotenv() # used for setting up the environment variable for the project
# print(os.getenv("PATH"))
# config = configparser.ConfigParser(interpolation=None)
# config.read('config.ini')
 
# user = config.get('DEFAULT', 'UserName')
# password = config.get('DEFAULT', 'Password')
# host = config.get('DEFAULT', 'Host')

user =os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")

TOPICS={
    "temperature": "Waterloo/Warehouse/{sensor_name}/temperature",
    "voltage": "Waterloo/Warehouse/{sensor_name}/voltage",
    "battery": "Waterloo/Warehouse/{sensor_name}/battery",
    "signal_strength": "Waterloo/Warehouse/{sensor_name}/signal_strength",
    "data_message_guid": "Waterloo/Warehouse/{sensor_name}/MessageID",
    "sensor_id":"Waterloo/Warehouse/{sensor_name}/sensor_id",
    "message_date": "Waterloo/Warehouse/{sensor_name}/message_date",
    "state": "Waterloo/Warehouse/{sensor_name}/state",
    "signal_strength": "Waterloo/Warehouse/{sensor_name}/signal_strength",
    "voltage": "Waterloo/Warehouse/{sensor_name}/voltage",
    "battery": "Waterloo/Warehouse/{sensor_name}/battery",
    "temperature": "Waterloo/Warehouse/{sensor_name}/temperature",
    "display_temperature": "Waterloo/Warehouse/{sensor_name}/display_temperature",
    "plot_temperature": "Waterloo/Warehouse/{sensor_name}/plot_temperature",
    "met_notification_requirements": "Waterloo/Warehouse/{sensor_name}/met_notification_requirements",
    "gateway_id": "Waterloo/Warehouse/{sensor_name}/gateway_id",
    "data_values": "Waterloo/Warehouse/{sensor_name}/data_values",
    "data_types": "Waterloo/Warehouse/{sensor_name}/data_types",
    "plot_values": "Waterloo/Warehouse/{sensor_name}/plot_values",
    "plot_labels": "Waterloo/Warehouse/{sensor_name}/plot_labels",
    "allsensor_data": "Waterloo/Warehouse/allsensor_data" ,
   

    
}

sensors= {
     "Room": thermostat("Room", (20.0, 25.0), battery_drain_cycle=100),
     "Refrigerator": thermostat("Refrigerator", (2.0, 5.0), battery_drain_cycle=150),
     "Freezer": thermostat("Freezer", (-18.0, -15.0), battery_drain_cycle=200),
}



def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message published. MID: {mid}, Reason Code: {reason_code}")

# function name:publish_sensorData(client)
# Description:This function  is used to publish all the sensor data as based on the topic and the key mapping 
# Parameter:void:self
# return:none
def publish_sensorData(client):

    key_mapping = {
        "data_message_guid":"MessageID",
        "sensor_id": "SensorID",
        "message_date": "MessageDate",
        "state": "State",
        "signal_strength": "SignalStrength",
        "voltage": "Voltage",
        "battery": "Battery",
        "temperature": "Data",
        "display_temperature": "DisplayData",
        "plot_temperature": "PlotValue",
        "met_notification_requirements": "MetNotificationRequirements",
        "gateway_id": "GatewayID",
        "data_values": "DataValues",
        "data_types": "DataTypes",
        "plot_values": "PlotValues",
        "plot_labels": "PlotLabels",
       

        
    }

    for sensor_name, sensor_instance in sensors.items():
        data =  sensor_instance.generate_sensor_data()
        if data is None:
            print(f"{sensor_name} has shut down.")
            continue

        result = json.loads(data)["Result"][0]
        for key, topic_template in TOPICS.items():
            if key not in key_mapping:
               continue
            topic = topic_template.format(sensor_name=sensor_name)
            mapped_key = key_mapping[key] 
            # payload = result[mapped_key]
            payload = result.get(mapped_key)
            if payload is not None:
                client.publish(topic, payload, qos=1)
                print(f"Published to {topic}: {payload}")


# function name:publish_all_sensorData(client)
# Description:This function  is used to publish all the sensor data(maybe in  the future if we add motion sensor then it will include that too)
# Parameter:void:self
# return:none
def publish_all_sensorData(client):
   
   allsensor_data=[]
   
   for sensor_name,thermostat_instance in sensors.items():
      data=thermostat_instance.generate_sensor_data()
      if data is None:
         print(f"{sensor_name} has shut down")
         continue
      # we are parsing through the sensor data and appending it to the list
      final_result=json.loads(data)["Result"][0]
      sensor_Data={
         "sensor_name":sensor_name,
         "data":final_result
      }
      allsensor_data.append(sensor_Data)
      print(allsensor_data)
      topics=TOPICS["allsensor_data"]
      payload=json.dumps(allsensor_data)
      client.publish(topics,payload,qos=1)
      print(f"Published all sensor data to {topics}:{payload}")





if __name__ == "__main__":
    client = paho.Client(callback_api_version= CallbackAPIVersion.VERSION2, client_id="", clean_session=True)
    client.tls_set() 
    client.username_pw_set(user, password)

    client.on_publish = on_publish
    client.connect(host, 8883)
    client.loop_start()
    try:
        #for i in range(1,3): # test code
        while TOPICS:
            publish_sensorData(client)
            if "allsensor_data" in TOPICS:
               publish_all_sensorData(client)
            time.sleep(3)
    except KeyboardInterrupt:
     print("Exiting...")
    finally:
     client.loop_stop()  
     client.disconnect()  # Disconnect the client

