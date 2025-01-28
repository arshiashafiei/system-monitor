import socket
import psutil
import time
import threading


def send_system_info(master_socket):
    request_body = "Hey agent, how's life treating you? Respond with 'Alive and Kicking' or 'Need Help'!"
    while True:
        question = master_socket.recv(1024).decode()
        print("QUESTION:")
        print(question)
        print(request_body)
        if question == request_body:
            try:
                # Get system information
                memory = psutil.virtual_memory()
                cpu = psutil.cpu_percent(interval=1)
                processes = len(psutil.pids())
                print("QUESTIONAAAAAAAAAAAAAAAAAa:")

                info = f"CPU: {cpu}%, Memory: {memory.percent}%, Processes: {processes}"
                master_socket.send(info.encode())
                print("QUESTIONAAAAAAAAAAAAAAAAAakdsajfvbdsavba:")
                # # Check for high usage and send UDP alert if necessary
                # if cpu > 80 or memory.percent > 80:
                #     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                #     udp_socket.sendto(f"High usage detected: CPU {cpu}%, Memory {memory.percent}%".encode(), (UDP_IP, UDP_PORT))
            except Exception as e:
                print(f"Error sending system info: {e}")
                break


def udp_alert_sender(UDP_IP, UDP_PORT):
    while True:
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)

        if cpu > 80 or memory.percent > 40:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(f"High usage detected: CPU {cpu}%, Memory {memory.percent}%".encode(), (UDP_IP, UDP_PORT))
        else:
            break


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
    threading.Thread(target=udp_alert_sender, args=(UDP_IP, UDP_PORT), daemon=True).start()

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
