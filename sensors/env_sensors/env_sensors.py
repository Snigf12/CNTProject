import threading
import os
import sys
# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from .transmission import send_to_main_server
import random
import time

class EnvSensors:
    def __init__(self):
        # Initialize global flag to indicate whether the program should stop
        self.stop_flag = False

    def generate_data_for_tandh_sensor(self):
        # Function to generate data for tandh_sensor
        # emulating device Sensirion SHT31 which for
        # Temperture sensor has a range -40°C to 125°C
        # Humidity sensor has a range of 0 %RH (relative humidity)
        # Emulation mode: room with average and normal
        # temperature and humidity of: 20°C - 26°C and 35 %RH to 50 $RH
        # Alerts will be shown when outside those ranges.
        
        # Define the probabilities for different temperature ranges
        tranges = [(-40, 0),(0, 25), (25, 30), (30, 125)]
        tprobabilities = [0.05, 0.1, 0.8, 0.05] #sum 100%
        
        # Define the probabilities for different humidity ranges
        hranges = [(0, 35),(35, 55), (55, 70), (70, 100)]
        hprobabilities = [0.05, 0.8, 0.1, 0.05] #sum 100%

        # Choose a temperature range based on the probabilities
        min_temp, max_temp = random.choices(population=tranges, weights=tprobabilities)[0]
        min_hum, max_hum = random.choices(population=hranges, weights=hprobabilities)[0]
        # Generate a random temperature within the chosen range
        temperature = round(random.uniform(min_temp, max_temp),1)
        humidity = round(random.uniform(min_hum, max_hum),1)
        return str(temperature)+"°C,"+str(humidity)+"%RH" # the structure is string i.g. 40°C,35%RH
        

    def generate_data_for_nl_sensor(self):
        # emulating device ZIO QWIIC LOUDNESS SENSOR (I2C) (101957)
        # Noise measure range 7.6dB - 100dB
        # Emulation mode: room with average and normal
        # noise levels in a workplace are between 40 dB to 60 dB
        # Alerts will be shown when outside over 60dB.
        
        # Define the probabilities for different temperature ranges
        nlranges = [(7.6, 40),(40, 60), (60, 90), (90, 100)]
        nlprobabilities = [0.1, 0.8, 0.07, 0.03] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_noise, max_noise = random.choices(population=nlranges, weights=nlprobabilities)[0]

        # Generate a random temperature within the chosen range
        noise = round(random.uniform(min_noise, max_noise),1) #One decimal value

        return str(noise)+"dB" # the structure is string i.g. 40dB


    def generate_data_for_li_sensor(self):
        # emulating device ZIO QWIIC TSL2561 sensor
        # Light intensity range from 0.1 - 40,000 lux on the fly
        # Emulation mode: room with average and normal
        # light levels in a workplace are between 500 - 1000 lux
        # Alerts will be shown when outside below 500 lux.
        
        # Define the probabilities for different temperature ranges
        liranges = [(0.1, 499),(500, 1000), (1000, 3000), (3000, 40000)]
        liprobabilities = [0.05, 0.9, 0.04, 0.01] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_light, max_light = random.choices(population=liranges, weights=liprobabilities)[0]

        # Generate a random temperature within the chosen range
        light = round(random.uniform(min_light, max_light),1) #One decimal value

        return str(light)+"Lux" # the structure is string i.g. 40°C,35%RH

    def data_generation_thread(self,device_name, sensor_name, protocol, data_generation_func):
        # Thread function for data generation and sending
        while not self.stop_flag:
            data = data_generation_func()
            send_to_main_server(device_name, sensor_name, data, protocol)
            time.sleep(1)  # Adjust sleep time as needed

    def start(self, device_name, protocol, sensors=[]):
        sensor_names = ["tandh_sensor", "nl_sensor", "li_sensor"]
        protocols = ["mqtt", "xmpp", "coap"]

        # Validate protocol value received is right
        if not isinstance(protocol, str):
            raise TypeError(f"{protocol} must be a string")
        if protocol not in protocols:
            raise ValueError(f"Invalid protocol: {protocol} it should be: mqtt, xmpp or coap")
        
        threads = []

        for value in sensors:
            if not isinstance(value, str):
                raise TypeError(f"{value} must be a string")
            if value not in sensor_names:
                raise ValueError(f"Invalid sensor name: {value} it should be: tandh_sensor, nl_sensor, li_sensor")

            print(f"Starting thread for {value}...")
            data_generation_func = getattr(self, f"generate_data_for_{value}")
            thread = threading.Thread(target=self.data_generation_thread, args=(device_name, value, protocol, data_generation_func))
            thread.start()
            threads.append(thread)

    def stop(self):
        self.stop_flag = True
        print("Environmental Sensors Turned-Off.")
