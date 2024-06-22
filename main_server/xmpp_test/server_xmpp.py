from slixmpp import ComponentXMPP
from slixmpp.xmlstream import JID

# Server details
server_address = "x.x.x.x"
server_port = 5554

# Username and password (replace with actual credentials)
username = "admin"
password = "!dr0ssw4P"

class MyXMPPServer(ComponentXMPP):
    def __init__(self, jid, password, server_address, server_port):
        super().__init__(jid, password)
        self.server_address = server_address
        self.server_port = server_port
        self.add_event_handler("session_start", self.handle_session_start)
        self.add_event_handler("message", self.handle_message)

    async def handle_session_start(self, event):
        self.send_presence()
        self.get_roster()

    async def handle_message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            self.send_message(mto=msg['from'], mbody="Received: %s" % msg['body'])

if __name__ == '__main__':
    jid = JID(username, server_address, "iotserver")  # Set a unique resource name
    xmpp = MyXMPPServer(jid, password, server_address, server_port)
    xmpp.connect((server_address, server_port))
    xmpp.process(forever=True)