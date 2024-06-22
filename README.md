# CNTProject
IoT Project to study CoAP, MQTT, and XMPP protocols - Unfinished

## The project was supposed to do the following:
A graphic user interface created using PyQT where the user should be able to add IoT devices with specific sensors, start or stop the emulation of the devices and the central server, and start transmitting data using one of the three protocols selected (CoAP, MQTT, or XMPP). The central server should start listening to these protocols and store the data in a PostgreSQL database.

The libraries used in the project were:
- aiocoap for the CoAP client and server.
- paho for the MQTT client and server.
- psycopg2 to integrate and manage the PostgreSQL database
- PyQT6 to develop the GUI (Still in progress)
- docker to manage docker instances (failed for now)
- slixmpp to manage XMPP client and server (still failing)

The emulation was supposed to create a Docker container for each IoT device and another one for the central server, and the communication had to start flowing between them.

## What is working:
1. The IoT sensors can be emulated locally, not in a Docker container, generating random "realistic" data and transmitting it using the specified protocol (Only CoAP and MQTT are working. XMPP is still being developed).
2. The central server can be emulated using WSL or locally and is able to act as CoAP and MQTT servers to listen for the data transmitted by the emulated sensors and store them in a PostgreSQL database.
3. The communication using CoAP and MQTT protocols, between locally emulated devices and the server deployed locally, WSL, or Virtual Machine in the same network as the IoT emulated devices.

## What is not working:
1. The XMPP protocol.
2. The integration with the GUI and the rest of the code.
3. The Docker containers that deploy separately the IoT sensors and central server.

## Quick test of the current state:
In the main server (recommended WSL - Ubuntu or in a VM)
1. Install all dependencies, PGAdmin, libraries paho, aiocoap, psycopg2. All in the machine you want to deploy the central server).
2. Run dbstart.py to create the database.
3. Run server_coap.py and server_mqtt.py
4. This will have the server all set.

In another VM with Ubuntu or even on local windows can work sometimes:
1. Install all dependencies, PGAdmin, libraries paho, aiocoap, psycopg2. All in the machine you want to deploy the IoT devices).
2. Check all the transmission.py files in each folder (air_sensors, env_sensors, and water_sensors) and change the server_ip = "x.x.x.x" variable with the Server's IP address. (Sorry about that, I should have added it to another file and manage this globally)
3. Run the testing_sensors.py -> the "sensors" will start transmitting data for 5 seconds and then will stop.

After this, you can check that the database is receiving the information and you can tell which ones used the CoAP protocol and which ones used MQTT. You can use Wireshark to see the packets and study how each protocol transmits the information.

If you want to run other tests, you can modify the devices by modifying this on the testing_sensors.py:
    airsensors.start("INPUTANYNAMEOFDEVICE","PROTOCOL" -> (coap, mqtt, xmpp-notworking*), ARRAYOFSENSORS -> depends on device (env, water or air sensors (see list of sensors in the files))
    e.g.
    airsensors.start("airsensor1","coap", ["co_sensor", "co2_sensor","no2_sensor"])
    envsensors.start("Env_sensor", "coap",["tandh_sensor","nl_sensor",'li_sensor'])
    watersensors.start("waterSensor1","mqtt",["ph_sensor","do_sensor"])

You can modify the protocols and the array of sensors that can be attached. the names of the sensors are in each file water_sensors.py, env_sensors.py, and air_sensors.py which are the files that generate the data and uses the transmission function to send it to the server.

## What each file of the project does:
MainFolder (./)
│   app.py -----------------------> This file starts the GUI. 
|                                   Shows the main window (the GUI is still 
|                                   a work in progress and is not integrated with the backend)
|
│   create_iot_instances.py ------> This was supposed to manage the Docker instances and deploy the 
|                                   IoT devices in different Docker instances and start transmitting data.
|                                   (Work in progress)
|
│   database.ini -----------------> This contains the credentials to authenticate with the server
|                                   and the IP address and port to connect. DISCLAIMER: you shouldn't 
|                                   store these in a production environment. This contains credentials 
|                                   to authenticate with the database. It is better to have them in 
|                                   environmental variables and call them in the code using the OS library.
|
│   dbread.py --------------------> This was supposed to be part of the integration between the GUI and the
|                                   database to print the data of the information transmitted and captured by
|                                   the central server.
|
│   deploy_server.py -------------> This was supposed to manage the Docker instance that deploys the 
|                                   central server and starts listening to the data transmitted by the clients.
|                                   (Work in progress)
|
│   requirements..txt ------------> These are the dependencies (libraries) to be installed in the local computer
|                                   that will run the final application when it is complete.
|
│   testing_sensors.py -----------> This is the way to use this application in the current stat. You can create
|                                   the objects you want. At this moment it creates three devices, which are
|                                   Air Sensors, Environmental Sensors, and Water sensors. The script
|                                   turns on the devices for 5 seconds, which start generating and transmitting data
|                                   according to the protocol they have, CoAP, CoAP, and MQTT respectively, 
|                                   and with the array, it says which sensors are gonna be transmitting. Then after 5s,
|                                   it turns off the device (stops transmitting).
|                                     e.g. airsensors.start("airsensor1","coap", ["co_sensor", "co2_sensor","no2_sensor"])
|                                          Here, we turn on the air sensor with name airsensor1, transmitting using CoAP protocol
|                                          and generating data for co, co2 and no2 sensors. (see sensors/air_sensors.py)
│
├───gui_src ----------------------> This folder contains all the GUI files developed using PyQT6 (Work in progress)
│       animated_toggle.py -------> This has the animation of the toggle button that turns on or off the IoT devices
|
│       main_window.py -----------> This has the code for the main window GUI. This is the first window the user sees
|                                   and it is deployed by app.py in the main folder
|
│       new_device.py ------------> This has a block that appears every time the add device is clicked to add
|                                   a new row to set up and turn on a new device.
│
├───main_server ------------------> This folder contains all the scripts for the Main Server that listens and
|   |                               has the database where it writes all the information.
|   |
│   │   database.ini -------------> Because this is supposed to become a whole new instance in a Docker container
|   |                               here is a duplicate information of the database user and password, and
|   |                               the IP address and port that is done when running the scripts. As mentioned before
|   |                               this is not good practice and should be managed differently in prod env.
|   |
│   │   dbstart.py ---------------> This is the first file to run when the server is with all the dependencies and
|   |                               ready. This will create the database if it doesn't exist and the table where
|   |                               the information gathered as CoAP, and MQTT server (later including XMPP) will be
|   |                               written in the created database.
|   |
│   │   Dockerfile ---------------> This is a Dockerfile to setup the main server, but it is still a work in progress.
|   |                               The file in the main folder deploy_server.py should use this Dockerfile to create the instance
|   |
│   │   insertdata.py ------------> This has the function of writing the information captured by the server_coap.py and server_mqtt.py
|   |                               (and server_xmpp.py in the future). Those servers use this file and the function in it to write
|   |                               the transmitted information into the database.
|   |
│   │   requirements.txt ---------> It has the dependencies that the server needs, and should be installed by the Dockerfile or by the
|   |                               server_config.sh file... still working on those Docker instances
|   |
│   │   server_coap.py -----------> It starts the CoAP server and starts listening to messages. When a payload is received, it uses the
|   |                               insertdata function in the insertdata.py file to write it into the database.
|   |
│   │   server_config.sh ---------> This is part of the attempts of using Docker. This should configure the server by installing
|   |                               the dependencies and software like pgadmin and python, and run the servers to start listening
|   |                               to the information, but it didn't work... this is still in progress.
|   |
│   │   server_mqtt.py ----------> Same as server_coap.py but using the paho library for MQTT.
|   |
│   │
│   └───xmpp_test ----------------> This is part of the development for XMPP server. It is a work in progress
│           server_xmpp.py -------> The file that's here is supposed to do the same as server_mqtt.py and 
|                                   server_coap.py but using slixmpp library. It is not working yet.
│
└───sensors ----------------------> This folder contains the scripts for all the IoT devices
    |                               (air sensors, environmental sensors, and Water sensors).
    |
    ├───air_sensors --------------> This is the folder to set up and deploy an air sensor device.
    |
    │       air_sensors.py -------> Here, the random "realistic" data generation is done.
    |                               each sensor "attached" to this device will generate
    |                               data and will use the transmission.py file and function to
    |                               transmit it to the main server.
    |                               
    │       client_coap.py -------> This is for testing. This piece of code is used in the transmission.py
    |                               It helps to test this protocol separately.
    |
    │       client_mqtt.py -------> Same as the previous file, it is used in the transmission.py file and
    |                               it is for testing the MQTT client transmitting messages to the server.
    |
    │       Dockerfile -----------> This is supposed to be used by the create_iot_instance.py file to deploy
    |                               the IoT device. This is a work in progress.
    |
    │       generate.py ----------> Ignore this for now... this is trying to see how to start running an IoT
    |                               device but specifying which sensors to be active just when the Docker
    |                               instance is deployed (work in progress)
    |
    │       requirements.txt -----> As this is gonna be in a separate Docker instance it needs the dependencies.
    |
    │       transmission.py ------> This receives the payload from the air_sensor.py generated data and transmits it
    |                               using the protocol specified in the main window (work in progress) or by the testing_sensors.py
    |                               in this case.
    │
    | THE NEXT BLOCKS HAVE THE SAME BEHAVIOUR AS THE AIR SENSOR. THEY WERE DONES SEPARATELY, BECAUSE EACH SENSOR (ALL FILES) SHOULD
    | BE STORED IN THE NEW DOCKER INSTANCE.
    ├───env_sensors
    │       client_coap.py
    │       client_mqtt.py
    │       Dockerfile
    │       env_sensors.py
    │       generate.py
    │       requirements.txt
    │       transmission.py
    │
    ├───water_sensors
    │       client_coap.py
    │       client_mqtt.py
    │       Dockerfile
    │       requirements.txt
    │       transmission.py
    │       water_sensors.py
    │
    └───xmpp_Test ----------> Work in progress to use XMPP as a client and be able to transmit using this protocol.
            client_xmpp.py
