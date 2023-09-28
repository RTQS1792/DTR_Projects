'''
Author: Hanqing Qi
Date: 2023-06-02 16:30:00
LastEditors: Hanqing Qi
LastEditTime: 2023-06-02 17:03:36
FilePath: /Blimps_Team/Python/UDP_Example/UDP_Server.py
Description: This is the UDP server to test the network connection between ESP32 and PC
'''
import socket

def udp_server():
    # Define the IP address and port
    ip_address = '192.168.0.41'  # or use '0.0.0.0' to listen on all available interfaces
    port = 8848  # Replace with your port

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (ip_address, port)
    server_socket.bind(server_address)
    print(f"Server is listening on {ip_address}:{port}")

    while True:
        # Wait for a connection
        print("waiting to receive message")
        data, address = server_socket.recvfrom(4096)
        print(f"received {len(data)} bytes from {address}")
        print(data)

udp_server()
