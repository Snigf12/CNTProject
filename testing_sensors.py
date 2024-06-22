import time
from sensors.air_sensors.air_sensors import AirSensors
from sensors.env_sensors.env_sensors import EnvSensors
from sensors.water_sensors.water_sensors import WaterSensors

airsensors = AirSensors()
envsensors = EnvSensors()
watersensors = WaterSensors()

try:
    airsensors.start("airsensor1","coap", ["co_sensor", "co2_sensor","no2_sensor"])
    envsensors.start("Env_sensor", "coap",["tandh_sensor","nl_sensor",'li_sensor'])
    watersensors.start("waterSensor1","mqtt",["ph_sensor","do_sensor"])
except ValueError as ve:
    print("ValueError:", ve)
except TypeError as te:
    print("TypeError:", te)

time.sleep(5)

airsensors.stop()
envsensors.stop()
watersensors.stop()