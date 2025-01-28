import socket
import threading
import time


def monitor_agent(client_socket, agent_address):
    # Get UDP port information from the agent
    # udp_info = client_socket.recv(1024).decode()
    # print(udp_info + "=====")
    # udp_ip, udp_port = udp_info.split(":")
    # print(f"Agent UDP monitoring set up at {udp_ip}:{udp_port}")
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


def ask_agent(client_socket, agent_address):
    # Get UDP port information from the agent
    # udp_info = client_socket.recv(1024).decode()
    # print(udp_info + "=====")
    # udp_ip, udp_port = udp_info.split(":")
    # print(f"Agent UDP monitoring set up at {udp_ip}:{udp_port}")
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


if __name__ == "__main__":
    MASTER_IP = "0.0.0.0"
    MASTER_PORT = 8888
    UDP_PORT = 8080

    # Start UDP alert listener in a separate thread
    threading.Thread(target=udp_alert_listener, args=(MASTER_IP, UDP_PORT), daemon=True).start()

    # Set up TCP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((MASTER_IP, MASTER_PORT))
    tcp_socket.listen(5)
    print(f"Master server listening on {MASTER_IP}:{MASTER_PORT}")

    while True:
        client_socket, agent_address = tcp_socket.accept()
        print(f"Connection established with agent {agent_address}")
        client_socket.send(f"{MASTER_IP}:{UDP_PORT}".encode())  # Send UDP info to agent
        threading.Thread(target=monitor_agent, args=(client_socket, agent_address), daemon=True).start()
