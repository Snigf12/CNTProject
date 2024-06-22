import paho.mqtt.client as mqtt
import asyncio
from aiocoap import *
from aiocoap.numbers.codes import POST

def send_to_main_server(device_name, sensor_name, data, protocol):
    print(f"Transmiting {data} from {device_name}, data from sensor {sensor_name} to server using {protocol} protocol")
    #return 0

    server_ip = "x.x.x.x" #USE the IP of the server

    # Function to send data to main server
    if (protocol == 'mqtt'):
        # Create an MQTT client instance
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Connect to the MQTT broker
        client.connect(server_ip, 1883, 60)  # Example broker, change to your broker address

        # Publish a message
        # Structure of the payload: String:"deviceName,sensor,value,value2*,protocol,status"
        client.publish("MQTT_message", f"{device_name},{sensor_name},{data},{protocol},OK")

        # Disconnect from the broker
        client.disconnect()

    elif (protocol == 'coap'):
        async def send():
            #print("I am sending coap messages!!")
            coap = await Context.create_client_context()

            # Structure of the payload: String:"deviceName,sensor,value,value2*,protocol,status"
            payload = f"{device_name},{sensor_name},{data},{protocol},OK"
            resource = "COAP_message"

            request = Message(code=POST, payload=payload.encode('utf-8'), uri=f"coap://{server_ip}/{resource}")
            response = await coap.request(request).response

            print("Response:", response.payload.decode('utf-8'))

        asyncio.run(send())
