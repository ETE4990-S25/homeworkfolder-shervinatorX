# python source file lab 10
import docker
import time
from datetime import datetime, timedelta

# Initialize Docker client (this lets us talk to Docker containers)
client = docker.from_env()

# Containers we want to monitor (this keeps things seperate)
containers_to_monitor = ["mysql", "adminer"]

# Store the last time we did a maintenance restart
last_restart = datetime.now()

# Function to check the status of each container
def check_container_status():
    """
    Checks if each container is running and displays its IP address.
    """
    print("Checking container statuses...")  # Just a simple print
    for container_name in containers_to_monitor:
        try:
            container = client.containers.get(container_name)  # Get the container
            if container.status == "running":  # If it's running
                networks = container.attrs['NetworkSettings']['Networks']
                # Loop through networks and display IP
                for net_name in networks:
                    net_data = networks[net_name]
                    print("{} is running in network '{}' with IP: {}".format(
                        container_name, net_name, net_data['IPAddress']))
            else:
                print("{} is not running.".format(container_name))
        except docker.errors.NotFound:
            print("{} not found in Docker.".format(container_name))
        except Exception as e:
            print("Error with {}: {}".format(container_name, str(e)))
    print("-" * 40)

# Function to relaunch a container if it is not running
def relaunch_container(container_name):
    """
    Relaunches the specified container if it is not running.
    """
    print("Attempting to relaunch container: {}".format(container_name))
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            print("Relaunching {}...".format(container_name))
            container.start()
            print("{} is now running.".format(container_name))
        else:
            print("{} is already running.".format(container_name))
    except docker.errors.NotFound:
        print("{} not found. Cannot relaunch.".format(container_name))
    except Exception as e:
        print("Error relaunching {}: {}".format(container_name, str(e)))

# Function to perform a maintenance restart after 24 hours
def maintenance_restart():
    """
    Restarts the containers if 24 hours have passed.
    """
    global last_restart
    time_since_last_restart = datetime.now() - last_restart
    if time_since_last_restart >= timedelta(days=1):
        print("24 hours have passed. Performing a maintenance restart.")
        for container_name in containers_to_monitor:
            try:
                container = client.containers.get(container_name)
                print("Restarting {}...".format(container_name))
                container.restart()
                print("{} has been restarted.".format(container_name))
            except Exception as e:
                print("Could not restart {}: {}".format(container_name, str(e)))
        last_restart = datetime.now()

# Main loop to continuously check, relaunch, and restart
while True:
    print("=== Docker Container Monitor ===")
    print("Current time: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Check each container
    check_container_status()
    
    # Try to relaunch if it's not running
    for container_name in containers_to_monitor:
        relaunch_container(container_name)
    
    # Do a maintenance restart every 24 hours
    maintenance_restart()
    
    print("Waiting for the next check... (10 minutes)")
    time.sleep(600)  # Wait for 10 minutes before checking again
