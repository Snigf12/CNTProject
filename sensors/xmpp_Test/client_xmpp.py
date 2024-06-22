from slixmpp import Jid, Xmpp
from slixmpp.exceptions import XMPPError

# Server details
server_address = "x.x.x.x"
server_port = 5554

# Username and password (replace with your actual credentials)
username = "admin"
password = "!dr0ssw4P"

# Message to send
message_content = "Hi! I am SENSOR_TEST and my temperature is 40°C"


class Client(Xmpp):
    def __init__(self, username, password):
        super().__init__(Jid(username, server_address, resource="client"))
        self.username = username
        self.password = password

        self.add_event_handler("session_status", self.handle_session_status)

    def handle_session_status(self, event):
        if event.get("reason") == "connected":
            self.send_message(Jid(server_address, server_address), message_content)
            self.disconnect()
        else:
            print(f"Failed to connect: {event.get('reason')}")

    def connect(self, server, port, secure=False):
        try:
            super().connect(server, port, secure)
            super().authenticate(self.username, self.password)
        except XMPPError as e:
            print(f"Error connecting: {e.message}")

if __name__ == "__main__":
    client = Client(username, password)
    client.connect(server_address, server_port)