# FILE :thermostat.py
# PROJECT :Wharehouse Watcher
# PROGRAMMER : Amel korandippillil Sunil
# FIRST VERSION : 
# DESCRIPTION :This basically conisist of a class which simulates a temperature sensor.


import random
import uuid
import time
import json



class thermostat:
    def __init__(self,sensor_name,temp_range):
        self.sensor_name=sensor_name
        self.temp_range=temp_range
        self.sensor_id=str(uuid.uuid4)
        self.battery=100 #getting started with full battery
        self.base_voltage=4 # its maximum voltage
        self.base_signal_Strength=100 # strong signal