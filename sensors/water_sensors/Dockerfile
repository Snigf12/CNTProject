# Use the EMQ X base image
FROM emqx/emqx:5.5.1

# Install Python and any necessary dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Create a directory for the app
WORKDIR /app

# Copy requirements.txt and Python files into the container
COPY ./sensors/requirements.txt /app/requirements.txt
COPY ./sensors/your_python_files.py /app/your_python_files.py

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Startup command to start EMQ X and run Python application
CMD ["emqx", "start"] && ["python3", "your_python_files.py"]