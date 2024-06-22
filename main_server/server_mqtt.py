# This is MQTT Broker
import configparser
import paho.mqtt.client as mqtt
from insertdata import insertdata

# Define callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code "+str(rc))
    # Subscribe to the topic(s) I want to receive messages from
    client.subscribe("MQTT_message")

def on_message(client, userdata, msg):
    

    payload = str(msg.payload.decode('utf8').strip())
    print("Received message on topic "+msg.topic+": "+ payload)
    print(payload)

    #DOING ALL THE QUERY TO THE DATABASE AND INSERT THE QUERY
    insertdata(payload)

    # Disconnect message -> when I receive stop as payload, the connection is stopped.
    #if payload == "stop":
    #    print("Exiting...")
    #    client.disconnect()

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Read connection details from database.ini
config = configparser.ConfigParser()
config.read('database.ini')

host = config['database']['host']

# Set up callback functions
client.on_connect = on_connect
client.on_message = on_message


try:
    # Connect to the MQTT broker
    client.connect(host, 1883, 60)  # Example broker address host and default ports, keepalive = 60

    # Blocking loop to listen for messages
    client.loop_forever()

except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()
