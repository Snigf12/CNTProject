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

class AirSensors:
    def __init__(self):
        # Initialize global flag to indicate whether the program should stop
        self.stop_flag = False

    def generate_data_for_co2_sensor(self):
        # emulating device Senseair K30 sensor
        # CO2 range from 0 - 5000 ppm
        # Emulation mode: Office room with average and normal
        # CO2 levels in a workplace are between 400 - 1000 ppm
        # Alerts will be shown when above 999 ppm.
        
        # Define the probabilities for different temperature ranges
        co2ranges = [(0, 400),(401, 999), (1000, 5000)]
        co2probabilities = [0.09, 0.9, 0.01] #sum 100%
        
        # Choose a temperature range based on the probabilities
        co2_min, co2_max = random.choices(population=co2ranges, weights=co2probabilities)[0]

        # Generate a random temperature within the chosen range
        co2 = round(random.uniform(co2_min, co2_max),1) #One decimal value

        return str(co2)+"ppm" # the structure is string i.g. 600ppm

    def generate_data_for_co_sensor(self):
        # emulating device SPEC-DGS-CO 968-034 sensor
        # CO range from 0 - 1000 ppm
        # Emulation mode: Home with average and normal
        # CO levels in average are between 0 - 30 ppm
        # Alerts will be shown when outside above 30 ppm.
        
        # Define the probabilities for different temperature ranges
        coranges = [(0, 30),(31, 1000)]
        coprobabilities = [0.95, 0.05] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_co, max_co = random.choices(population=coranges, weights=coprobabilities)[0]

        # Generate a random temperature within the chosen range
        co = round(random.uniform(min_co, max_co),1) #One decimal value

        return str(co)+"ppm" # the structure is string i.g. 10ppm

    def generate_data_for_no2_sensor(self):
        # emulating device SPEC-DGS-NO2 968-043 sensor
        # NO2 range from 0 - 5 ppm
        # Emulation mode: Desirable during the year
        # NO2 levels are between 0.03 - 0.05 ppm
        # Alerts will be shown when above 0.1 ppm.
        
        # Define the probabilities for different temperature ranges
        no2ranges = [(0, 0.029),(0.03, 0.05),(0.051, 0.1),(0.11,5)]
        no2probabilities = [0.03,0.95,0.015,0.005] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_no2, max_no2 = random.choices(population=no2ranges, weights=no2probabilities)[0]

        # Generate a random temperature within the chosen range
        no2 = round(random.uniform(min_no2, max_no2),3) #Three decimal valueS

        return str(no2)+"ppm" # the structure is string i.g. 0.032ppm

    def generate_data_for_o3_sensor(self):
        # emulating device DGS-O3 968-042 sensor
        # O3 range from 0 - 5 ppm
        # Emulation mode: Desirable level in rooms
        # O3 levels are good between 0 - 0.054 ppm
        # Alerts will be shown when above 0.055 ppm.
        # Above 0.086 is unhealthy
        
        # Define the probabilities for different temperature ranges
        o3ranges = [(0, 0.05),(0.051, 0.086),(0.086,5)]
        o3probabilities = [0.95,0.045,0.005] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_o3, max_o3 = random.choices(population=o3ranges, weights=o3probabilities)[0]

        # Generate a random temperature within the chosen range
        o3 = round(random.uniform(min_o3, max_o3),3) #Three decimal valueS

        return str(o3)+"ppm" # the structure is string i.g. 0.03ppm

    def data_generation_thread(self, device_name, sensor_name, protocol, data_generation_func):
        # Thread function for data generation and sending
        while not self.stop_flag:
            data = data_generation_func()
            send_to_main_server(device_name, sensor_name, data, protocol)
            time.sleep(1)  # Adjust sleep time as needed

    def start(self, device_name, protocol, sensors=[]):
        sensor_names = ["co2_sensor", "co_sensor", "no2_sensor", "o3_sensor"]
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
                raise ValueError(f"Invalid sensor name: {value} it should be: co2_sensor, co_sensor, no2_sensor or o3_sensor")

            print(f"Starting thread for {value}...")
            data_generation_func = getattr(self, f"generate_data_for_{value}")
            thread = threading.Thread(target=self.data_generation_thread, args=(device_name, value, protocol, data_generation_func))
            thread.start()
            threads.append(thread)

    def stop(self):
        self.stop_flag = True
        print("Air Sensors Turned-Off.")
