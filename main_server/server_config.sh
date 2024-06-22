#!/bin/bash

# Install PostgreSQL and set password
sudo apt-get update
sudo apt-get install -y postgresql python3 python3-pip libssl-dev libcoap3 libcoap3-dev libcoap3-bin curl prosody libpq-dev libnss3 libgbm1 libgbm-dev
sudo -u postgres psql -c "ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';"
sudo systemctl restart postgresql.service

# Install pgAdmin
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
sudo apt install pgadmin4
sudo /usr/pgadmin4/bin/setup-web.sh

# Run the Python script for starting the database
python3 dbstart.py &

# Wait for a moment before starting the other scripts
sleep 5

# Run the Python script for CoAP server in a new terminal session
gnome-terminal -- python3 server_coap.py

# Run the Python script for MQTT server in a new terminal session
gnome-terminal -- python3 server_mqtt.py