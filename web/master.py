import requests

def get_system_status(agent_url):
    try:
        response = requests.get(f"{agent_url}/status")
        response.raise_for_status()
        data = response.json()
        print("\nSystem Status:")
        print(f"CPU Usage: {data['cpu']}%")
        print(f"Memory Usage: {data['memory']}%")
        print(f"Number of Processes: {data['processes']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching system status from {agent_url}: {e}")

def restart_system(agent_url):
    try:
        response = requests.post(f"{agent_url}/restart")
        response.raise_for_status()
        print("\nRestart Response:")
        print(response.json()["message"])
    except requests.exceptions.RequestException as e:
        print(f"Error restarting system at {agent_url}: {e}")

if __name__ == "__main__":
    # URL of the agent's web service
    agent_url = "http://127.0.0.1:8000"  # Replace with the actual agent URL

    while True:
        print("\nCentral Management System")
        print("1. Get System Status")
        print("2. Restart System")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            get_system_status(agent_url)
        elif choice == "2":
            restart_system(agent_url)
        elif choice == "3":
            print("Exiting Central Management System.")
            break
        else:
            print("Invalid choice. Please try again.")
