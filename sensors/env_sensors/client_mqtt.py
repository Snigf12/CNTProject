import paho.mqtt.client as mqtt

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Connect to the MQTT broker
client.connect("x.x.x.x", 1883, 60)  # Example broker, change to your broker address

# Publish a message
# Structure of the payload: String:"deviceName,sensor,value,value2*,protocol,status"
client.publish("MQTT_message", "Device1,tandh_sensor,40°C,35%RH,CoAP,OK")
client.publish("MQTT_message", "Device2,tandh_sensor,25°C,55%RH,CoAP,OK")
client.publish("MQTT_message", "Device1,nl_sensor,15dB,CoAP,OK")
#client.publish("IoTSensor", "stop") #end connection

# Disconnect from the broker
client.disconnect()
