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
    def __init__(self,sensor_name,temp_range,battery_drain_cycle):
        self.sensor_name=sensor_name
        self.temp_range=temp_range
        self.sensor_id=str(uuid.uuid4)
        self.battery=100 #getting started with full battery
        self.base_voltage=4 # its maximum voltage
        self.base_signal_Strength=100 # strong signal
        self.battery_drain_cycle=battery_drain_cycle # its basically gives the number of cycles until battery drains completely
        self.drain_per_cycle=100/battery_drain_cycle

    # function name:temperataure_generater(self)
    # Description:This funciton is used to provide us with the temperature
    # Parameter:void:
    # return:int number:battery.


    def temperataure_generater(self):
        return round(random.uniform(*self.temp_range), 1)
    
        
    # function name:battery_updates()
    # Description:This function is used to simulate and  update the battey drain and life
    # Parameter:void:self
    # return:int number:battery.

    def battery_updates(self):
        if self.battery>0:
           self.base_signal_Strength=max(0,self.base_battery-random.uniform(0.001,0.1))
        return round(self.battery,2)
        
    