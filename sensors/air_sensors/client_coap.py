import asyncio
from aiocoap import *
from aiocoap.numbers.codes import POST


async def main():
    protocol = await Context.create_client_context()

    server_ip = "x.x.x.x"
    payload = "Device1,tandh_sensor,40°C,35%RH,coap,OK"
    resource = "COAP_message"

    request = Message(code=POST, payload=payload.encode('utf-8'), uri=f"coap://{server_ip}/{resource}")
    response = await protocol.request(request).response

    print("Response:", response.payload.decode('utf-8'))

if __name__ == '__main__':
    asyncio.run(main())
