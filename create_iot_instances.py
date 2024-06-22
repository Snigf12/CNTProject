import docker
import time
import os

# This class will create an object which will be a docker container that executes one of the python sensors
class Device:
    def __init__(self, lbDevice, lbDeviceType, protocol, sensors) -> None:
        self.devicename = lbDevice
        self.dockerfile = os.path.join(".", "sensors\\", lbDeviceType+"\\") #path to Dockerfile
        print(self.dockerfile)
        SENSORS = ",".join(sensors)
        #This will excecute the devices seting the arguments of the Dockerfile
        self.build_args = {
            'PROTOCOL': protocol,
            'SENSORS': SENSORS
        }
        self.deployDevice()

    #create docker image and container
    def deployDevice(self):
        #creates docker client
        self.client = docker.from_env()
        #build image from Dockerfile
        self.image = self.client.images.build(path=self.dockerfile, buildargs=self.build_args, tag=self.devicename)
        self.imId = self.image.id
        #Run image to create instance
        self.container = self.client.containers.run(image=self.devicename, command=['python3', 'generate.py', '$PROTOCOL', '$SENSORS'], detach=True)
        self.contId = self.container.id


    #Destroy docker image and container
    def destroyDevice(self):
        # Delete the container
        try:
            self.container.remove(force=True)
            print("Container deleted successfully.")
        except docker.errors.NotFound:
            print("Container not found.")
        #Delete Image
        try:
            self.image.remove(image=self.imId, force=True)
            print("Image deleted successfully.")
        except docker.errors.ImageNotFound:
            print("Image not found.")

    #Only stops container to stop generating and sensing data
    def stopDevice(self):
        try:
            self.container.stop()
            print("Container stopped successfully.")
        except docker.errors.NotFound:
            print("Container not found.")
    #This is when the container already exist
    def startDevice(self):
        try:
            self.container.start()
            print("Container stopped successfully.")
        except docker.errors.NotFound:
            print("Container not found.")

#Simulating the application GUI
lbDevice = "env_sensors1"
lbDeviceType = "env_sensors"
protocol = "mqtt"
sensors = ["li_sensor","tandh_sensor","nl_sensor"]

device = Device(lbDevice, lbDeviceType, protocol, sensors)
device.deployDevice()

time.sleep(30)

device.destroyDevice()