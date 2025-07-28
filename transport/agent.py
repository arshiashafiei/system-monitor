import socket
import psutil
import threading


def send_system_info(master_socket):
    request_body = "Hey agent, how's life treating you? Respond with 'Alive and Kicking' or 'Need Help'!"
    while True:
        question = master_socket.recv(1024).decode()

        if question == request_body:
            try:
                memory = psutil.virtual_memory()
                cpu = psutil.cpu_percent(interval=1)
                processes = len(psutil.pids())

                info = f"CPU: {cpu}%, Memory: {memory.percent}%, Processes: {processes}"
                master_socket.send(info.encode())
            except Exception as e:
                print(f"Error sending system info: {e}")
                break
        elif question == "restart":
            try:
                # os.system("reboot")
                print("system restarted!!!!!!!!!!!!!!!!!!!!!:")
            except Exception as e:
                print(f"Error sending system info: {e}")
                break


def udp_alert_sender(UDP_IP, UDP_PORT):
    while True:
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)

        if cpu > 80 or memory.percent > 40:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(
                f"High usage detected: CPU {cpu}%, Memory {memory.percent}%".encode(),
                (UDP_IP, UDP_PORT))
        else:
            break


def master_broadcast_listener(ip, udp_port, tcp_ip, tcp_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("", udp_port))
    print(f"Listening for broadcast responses on {udp_port}")
    while True:
        message = udp_socket.recv(1024)
        if message.decode() == "Is it just me, or did something just move on this network?":
            udp_socket.sendto(
                f"{tcp_ip}:{tcp_port}".encode(),
                ("255.255.255.255", udp_port + 1))


if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    AGENT_IP = local_ip
    TCP_PORT = 8888
    broadcast_port = 8080

    threading.Thread(target=master_broadcast_listener,
                     args=(AGENT_IP, broadcast_port, AGENT_IP, TCP_PORT),
                     daemon=True).start()
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((AGENT_IP, TCP_PORT))
    tcp_socket.listen(5)
    print(f"Agent server listening on {AGENT_IP}:{TCP_PORT}")

    while True:
        try:
            master_socket, master_address = tcp_socket.accept()
            print(f"Connection established with Master {master_address}")

            udp_info = master_socket.recv(1024).decode()
            UDP_IP, UDP_PORT = udp_info.split(":")
            UDP_PORT = int(UDP_PORT)

            print(f"Connected to master. UDP alerts will be sent to \
                   {UDP_IP}:{UDP_PORT}")
            threading.Thread(target=send_system_info, args=(master_socket, ),
                             daemon=True).start()
            threading.Thread(target=udp_alert_sender, args=(UDP_IP, UDP_PORT),
                             daemon=True).start()
        except KeyboardInterrupt:
            print("Shutting down agent...")
            master_socket.close()
            break
