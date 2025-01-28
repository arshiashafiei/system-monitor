import socket
import psutil
import time
import threading


def send_system_info(master_socket):
    while True:
        try:
            # Get system information
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            processes = len(psutil.pids())

            info = f"CPU: {cpu}%, Memory: {memory.percent}%, Processes: {processes}"
            master_socket.send(info.encode())

            # Check for high usage and send UDP alert if necessary
            if cpu > 80 or memory.percent > 80:
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.sendto(f"High usage detected: CPU {cpu}%, Memory {memory.percent}%".encode(), (UDP_IP, UDP_PORT))
        except Exception as e:
            print(f"Error sending system info: {e}")
            break
        time.sleep(5)


if __name__ == "__main__":
    MASTER_IP = "127.0.0.1"  # Change this to the master's IP
    MASTER_PORT = 8888

    # Connect to master server via TCP
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.connect((MASTER_IP, MASTER_PORT))

    # Receive UDP info from the master
    udp_info = master_socket.recv(1024).decode()
    UDP_IP, UDP_PORT = udp_info.split(":")
    UDP_PORT = int(UDP_PORT)

    print(f"Connected to master. UDP alerts will be sent to {UDP_IP}:{UDP_PORT}")

    # Start sending system info
    threading.Thread(target=send_system_info, args=(master_socket,), daemon=True).start()

    # Keep the connection alive
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down agent...")
            master_socket.close()
            break
