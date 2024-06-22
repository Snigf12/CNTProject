# Use the python base image
FROM python:3.11.2

# Install Python and any necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 \
                       python3-pip \
                       libssl-dev

# Create a directory for the app
WORKDIR /app

# Copy requirements.txt and Python files into the container
COPY ../../requirements.txt /app/requirements.txt
COPY ./air_sensors.py /app/sensors/air_sensors/air_sensors.py
COPY ../air_sensors.py /app/sensors/client_coap.py

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.

# Set default values for build arguments
ARG PROTOCOL=mqtt
ARG SENSORS=co2_sensor,co_sensor,no2_sensor,o3_sensor

# Convert the comma-separated list of sensors to an array in the shell script
CMD ["bash", "-c", "python3 generate.py $PROTOCOL $SENSORS"]