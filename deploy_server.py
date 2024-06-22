import os
import docker

def build_and_run_container(dockerfile_path, image_name, container_name):
    # Create a Docker client
    client = docker.from_env()

    # Build the Docker image from the Dockerfile
    image, build_logs = client.images.build(path=dockerfile_path, tag=image_name)

    # Run the container from the built image
    container = client.containers.run(image=image_name, detach=True, name=container_name)

    return container

if __name__ == "__main__":
    # Path to the directory containing the Dockerfile
    dockerfile_path = os.path.join(os.path.dirname(__file__), "main_server")


    # Name of the Docker image to build
    image_name = "emqx"

    # Name of the Docker container
    container_name = "iot_server"

    # Build and run the Docker container
    container = build_and_run_container(dockerfile_path, image_name, container_name)

    print("Container ID:", container.id)
