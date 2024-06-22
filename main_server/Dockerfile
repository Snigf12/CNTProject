# Use the EMQX base image
FROM ubuntu

# Create a directory for the app
WORKDIR /app/main_server

# Copy requirements.txt and Python files into the container
COPY ./requirements.txt /app/main_server/requirements.txt
COPY ./dbstart.py /app/main_server/dbstart.py
COPY ./server_coap.py /app/main_server/server_coap.py
COPY ./server_mqtt.py /app/main_server/server_mqtt.py
# COPY ./server_xmpp.py /app/main_server/server_xmpp.py
# COPY ./server_xmpp.py /app/main_server/database.ini
COPY ./database.ini /app/main_server/database.ini
COPY ./server_config.sh /app/main_server/server_config.sh

# Install Python and Python dependencies
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Startup command to start EMQ X and run Python application
CMD ["bash", "-c" ,"./server_config.sh"]
# && ["python3", "server_xmpp.py"] I commented until I solve and test this protocol.