# I get the arguments when running this file using sys and ast
# this way I can call the generate.py with python3 generate.py "mqtt" "sensor1, sensor2, sensor3"
import sys
import ast
import time

# import air_sensors
from env_sensors import EnvSensors

protocol = sys.argv[1]
deviceName = ast.literal_eval(sys.argv[2])
sensors = ast.literal_eval(sys.argv[3]) #converts string received as argument into an array

envsensors = EnvSensors()

try:
    envsensors.start(deviceName,protocol,sensors)
except ValueError as ve:
    print("ValueError:", ve)
    envsensors.stop()
except TypeError as te:
    print("TypeError:", te)
    envsensors.stop()

#comment this when docker is working so we stop just shuting down the container.
time.sleep(50)
envsensors.stop()