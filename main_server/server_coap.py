# This is my CoAP Server
import configparser
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
from insertdata import insertdata

logging.basicConfig(level=logging.INFO)

class IoTSensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.payload = b"Response from IoT Main Server"

    async def render_get(self, request):
        payload = request.payload.decode('utf-8')
        print("Received message:", payload)
        #DOING ALL THE QUERY TO THE DATABASE AND INSERT THE QUERY
        insertdata(payload)
        return aiocoap.Message(payload=self.payload)

    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        print("Received POST message:", payload)

        #DOING ALL THE QUERY TO THE DATABASE AND INSERT THE QUERY
        insertdata(payload)

        # Process the POST message payload in case it is successfull
        return aiocoap.Message(payload=b"POST message received successfully")

async def main():
    # Read connection details from database.ini
    config = configparser.ConfigParser()
    config.read('database.ini')

    host = config['database']['host']
    #print(host)

    # Specify the IP address and port of the CoAP server
    ip_address = "0.0.0.0" #host  # IP address of the server
    port = aiocoap.COAP_PORT  # Use the default CoAP port

    # Create the IoTSensorResource instance
    ioT_server = IoTSensorResource()

    # Create a Site and add the IoTSensorResource to it
    root = resource.Site()
    root.add_resource(('COAP_message',), ioT_server)

    # Create the CoAP server context with the specified IP address
    context = await aiocoap.Context.create_server_context(site=root, bind=(ip_address, port))

    print(f"CoAP server started and listening for messages on {ip_address}:{port}...")

    # Keep the event loop running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())