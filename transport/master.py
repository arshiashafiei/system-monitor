import socket
import threading
import time

AGENTS_IPS = []


def monitor_agent(client_socket, agent_address):
    time.sleep(0.5)
    restart_agent(client_socket, agent_address)
    while True:
        try:
            ask_agent(client_socket, agent_address)

            data = client_socket.recv(1024).decode()
            if data:
                print(f"Received from {agent_address}: {data}")
        except Exception as e:
            print(f"Error communicating with agent {agent_address}: {e}")
            break

    client_socket.close()
    print(f"Connection closed for agent {agent_address}")


def discover_agents(udp_port):
    while True:
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            message = "Is it just me, or did something just move on this network?".encode()

            print(f"Broadcasting message: {message} on port {udp_port}")

            udp_socket.sendto(message, ("255.255.255.255", udp_port))
            time.sleep(4)
        except Exception as e:
            print(f"Error broadcasting {e}")
            break


def agent_response_listener(udp_port):
    udp_port += 1
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("0.0.0.0", udp_port))
    print(f"Listening for broadcast responses on {udp_port}")
    while True:
        data, _ = udp_socket.recvfrom(1024)
        agent_ip, agent_port = data.decode().split(":")
        agent_port = int(agent_port)
        AGENTS_IPS.append((agent_ip, agent_port))
        print(f"response from {agent_ip}:{agent_port}")


def ask_agent(client_socket, agent_address):
    # Get UDP port information from the agent
    udp_info = client_socket.recv(1024).decode()
    print(udp_info + "=====")
    udp_ip, udp_port = udp_info.split(":")
    print(f"Agent UDP monitoring set up at {udp_ip}:{udp_port}")
    try:
        request_body = "Hey agent, how's life treating you? Respond with 'Alive and Kicking' or 'Need Help'!"

        client_socket.send(request_body.encode())
        time.sleep(2)
    except Exception as e:
        print(f"Error communicating with agent {agent_address}: {e}")

    print(f"Asking {agent_address}, How's life treating you?")


def udp_alert_listener(udp_ip, udp_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_ip, udp_port))
    print(f"Listening for UDP alerts on {udp_ip}:{udp_port}")
    while True:
        alert, addr = udp_socket.recvfrom(1024)
        print(f"ALERT from {addr}: {alert.decode()}")


def restart_agent(client_socket, agent_address):
    try:
        print(f"Asking {agent_address}, to RESTART.")
        request_body = "restart"

        client_socket.send(request_body.encode())
        time.sleep(2)
    except Exception as e:
        print(f"Error communicating with agent {agent_address}: {e}")


if __name__ == "__main__":
    MASTER_IP = "0.0.0.0"
    BROADCAST_PORT = 8080
    UDP_ALERT_PORT = 9090

    threading.Thread(target=discover_agents, args=(BROADCAST_PORT, ), daemon=True).start()
    threading.Thread(target=agent_response_listener, args=(BROADCAST_PORT, ), daemon=True).start()
    while True:
        try:
            if len(AGENTS_IPS) != 0:
                for agent in AGENTS_IPS:
                    # print(agent)
                    agent_ip,  agent_port = agent
                    # print(f"Connecting to agent {agent_ip}:{agent_port}")
                    agent_socket = socket.socket(socket.AF_INET,
                                                 socket.SOCK_STREAM)
                    agent_socket.connect((agent_ip, agent_port))

                    print(f"Connection established with agent {agent_ip}")
                    agent_socket.send(f"{MASTER_IP}:{UDP_ALERT_PORT}".encode())
                    threading.Thread(target=monitor_agent,
                                     args=(agent_socket, agent_ip),
                                     daemon=True).start()
            else:
                print("No agent reachable...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down socket...")
            agent_socket.close()
            break
