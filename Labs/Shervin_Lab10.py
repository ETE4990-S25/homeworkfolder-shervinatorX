import docker
import time
from datetime import datetime, timedelta

# Initialize Docker client
client = docker.from_env()

# List of containers to monitor
containers_to_monitor = ["mysql", "adminer"]

# Set the last restart time
last_restart = datetime.now()

def check_container_status():
    """
    Checks if each container is running and displays its IP address.
    """
    for container_name in containers_to_monitor:
        try:
            container = client.containers.get(container_name)
            if container.status == "running":
                networks = container.attrs['NetworkSettings']['Networks']
                for net_name, net_data in networks.items():
                    print(f"{container_name} in network '{net_name}' has IP: {net_data['IPAddress']}")
            else:
                print(f"⚠️ {container_name} is not running.")
        except docker.errors.NotFound:
            print(f"❌ {container_name} not found.")
        except Exception as e:
            print(f"⚠️ Error with {container_name}: {e}")
    print("-" * 40)

def relaunch_container(container_name):
    """
    Relaunches the specified container if it is not running.
    """
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            print(f"🔄 Relaunching {container_name}...")
            container.start()
            print(f"✅ {container_name} is now running.")
    except docker.errors.NotFound:
        print(f"❌ {container_name} not found. Cannot relaunch.")
    except Exception as e:
        print(f"⚠️ Error relaunching {container_name}: {e}")

def maintenance_restart():
    """
    Restarts the containers if 24 hours have passed.
    """
    global last_restart
    if datetime.now() - last_restart >= timedelta(days=1):
        print("🔄 Performing daily maintenance restart.")
        for container_name in containers_to_monitor:
            try:
                container = client.containers.get(container_name)
                print(f"🔄 Restarting {container_name}...")
                container.restart()
                print(f"✅ {container_name} has been restarted.")
            except Exception as e:
                print(f"⚠️ Could not restart {container_name}: {e}")
        last_restart = datetime.now()

# Main loop to continuously check and relaunch if necessary
while True:
    print(f"🔄 Checking containers at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    check_container_status()
    for container_name in containers_to_monitor:
        relaunch_container(container_name)
    maintenance_restart()
    time.sleep(600)  # Check every 10 minutes
