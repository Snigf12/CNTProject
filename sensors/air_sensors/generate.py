# I get the arguments when running this file using sys and ast
# this way I can call the generate.py with python3 generate.py "mqtt" "sensor1, sensor2, sensor3"
import sys
import ast

# import air_sensors
from air_sensors import AirSensors

protocol = sys.argv[1]
sensors = ast.literal_eval(sys.argv[2]) #converts string received as argument into an array

airsensors = AirSensors()

try:
    airsensors.start(protocol,sensors)
except ValueError as ve:
    print("ValueError:", ve)
    airsensors.stop()
except TypeError as te:
    print("TypeError:", te)
    airsensors.stop()