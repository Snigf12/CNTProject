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

class WaterSensors:
    def __init__(self):
        # Initialize global flag to indicate whether the program should stop
        self.stop_flag = False

    def generate_data_for_turb_sensor(self):
        # emulating device SEN0189 sensor
        # turb range from 0 - 3 NTU
        # Emulation mode: Desirable level in potable
        # water are safe when below 0.3 NTU with target of less than 0.1
        # Alerts will be shown when above 0.1 NTU.
        
        # Define the probabilities for different temperature ranges
        turbranges = [(0, 0.1),(0.1, 0.3),(0.3,3)]
        turbprobabilities = [0.95,0.045,0.005] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_turb, max_turb = random.choices(population=turbranges, weights=turbprobabilities)[0]

        # Generate a random temperature within the chosen range
        turb = round(random.uniform(min_turb, max_turb),2) #Two decimal valueS

        return str(turb)+"NTU" # the structure is string i.g. 0.04NTU

    def generate_data_for_ph_sensor(self):
        # emulating device SEN0161 DFRobot Analog pH Meter Kit
        # pH range from 0 - 14 (0 acid, 7 basic, 14 basic)
        # Emulation mode: Desirable level in potable
        # water are safe when between 7.0 10.5
        # Alerts will be shown when outside 7-10.5
        
        # Define the probabilities for different temperature ranges
        phranges = [(0, 7),(7, 10.5),(10.5,14)]
        phprobabilities = [0.025,0.095,0.025] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_ph, max_ph = random.choices(population=phranges, weights=phprobabilities)[0]

        # Generate a random temperature within the chosen range
        ph = round(random.uniform(min_ph, max_ph),1) #One decimal valueS

        return str(ph) # the structure is string i.g. 7.2

    def generate_data_for_ec_sensor(self):
        # emulating device EC-KIT-1.0 sensor
        # ec range from 5 µS/cm to 200,000 µS/cm (S=siemens)
        # Emulation mode: Desirable level in potable
        # water are safe when below 700 µS/cm
        # Alerts will be shown when above 700 µS/cm.
        
        # Define the probabilities ranges
        ecranges = [(0, 700),(700, 200000)]
        ecprobabilities = [0.99,0.01] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_ec, max_ec = random.choices(population=ecranges, weights=ecprobabilities)[0]

        # Generate a random temperature within the chosen range
        ec = round(random.uniform(min_ec, max_ec),1) #One decimal valueS

        return str(ec)+"µS/cm" # the structure is string i.g. 300µS/cm

    def generate_data_for_do_sensor(self):
        # emulating device Kit-103DX sensor
        # do range from 0.00 mg/L to 300 mg/L
        # Emulation mode: Desirable level in potable
        # water are safe when above 6.5 mg/L
        # on average 6.5 to 8 mg/L
        # Alerts will be shown when below 6.5 mg/L.
        
        # Define the probabilities for different temperature ranges
        doranges = [(0, 6.5),(6.5, 8),(8, 300)]
        doprobabilities = [0.01,0.98,0.01] #sum 100%
        
        # Choose a temperature range based on the probabilities
        min_do, max_do = random.choices(population=doranges, weights=doprobabilities)[0]

        # Generate a random temperature within the chosen range
        do = round(random.uniform(min_do, max_do),1) #One decimal valueS

        return str(do)+"µS/cm" # the structure is string i.g. 300µS/cm

    def data_generation_thread(self, device_name, sensor_name, protocol, data_generation_func):
        # Thread function for data generation and sending
        while not self.stop_flag:
            data = data_generation_func()
            send_to_main_server(device_name, sensor_name, data, protocol)
            time.sleep(1)  # Adjust sleep time as needed

    def start(self,device_name, protocol, sensors=[]):
        sensor_names = ["turb_sensor", "ph_sensor", "ec_sensor", "do_sensor"]
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
                raise ValueError(f"Invalid sensor name: {value} it should be: turb_sensor, ph_sensor, ec_sensor or do_sensor")

            print(f"Starting thread for {value}...")
            data_generation_func = getattr(self, f"generate_data_for_{value}")
            thread = threading.Thread(target=self.data_generation_thread, args=(device_name, value, protocol, data_generation_func))
            thread.start()
            threads.append(thread)

    def stop(self):
        self.stop_flag = True
        print("Water Sensors Turned-Off.")
