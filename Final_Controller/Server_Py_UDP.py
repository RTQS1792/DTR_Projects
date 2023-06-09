'''
Author: Hanqing Qi
Date: 2023-06-02 16:30:00
LastEditors: Hanqing Qi
LastEditTime: 2023-06-02 17:03:36
FilePath: /Blimps_Team/Python/UDP_Example/UDP_Server.py
Description: This is the UDP server that receives data from the receiver and control the vehicle
'''
import socket
import time
# Define the IP address and port
ip_address = '192.168.0.41'  # or use '0.0.0.0' to listen on all available interfaces
port = 8848  # Replace with your port

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (ip_address, port)
server_socket.bind(server_address)
print(f"Server is listening on {ip_address}:{port}")

CAR_IP = '192.168.0.204'
cars = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cars.connect((CAR_IP, 5000))
print('Cars connected')

Blind_Flag = 0

while True:
    # Wait for a connection
    # print(".")
    data, address = server_socket.recvfrom(4096)
    # print(f"received {len(data)} bytes from {address}")
    if len(data) == 2:
        Blind_Flag = 0
        if data[0] == 49 and data[1] == 48: # Left Target Right Blind
            command = 'CMD_MOTOR#-1100#-1100#1100#1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("←")
        elif data[0] == 49 and data[1] == 50: # Left Target Right Noise
            command = 'CMD_MOTOR#-1100#-1100#1100#1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("↖")
        elif data[0] == 50 and data[1] == 48: # Left Noise Right Blind
            command = 'CMD_MOTOR#-1100#-1100#1100#1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("↖")
        elif data[0] == 50 and data[1] == 49: # Left Noise Right Target
            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("↗")
        elif data[0] == 49 and data[1] == 49: # Target
            command = 'CMD_MOTOR#1100#1100#1100#1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("↑")
        elif data[0] == 50 and data[1] == 50: # Left Noise Right Noise
            command = 'CMD_MOTOR#1500#1500#-1500#-1500\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            print("↗")
    elif len(data) == 1:
        if data[0] == 48: # Left Blind Right Blind
            Blind_Flag += 1
            if Blind_Flag >= 10:
                command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                cars.send(command.encode('utf-8'))
                time.sleep(0.1)
                print("X")
            else:
                command = 'CMD_MOTOR#0#0#0#0\n'
                cars.send(command.encode('utf-8'))
                time.sleep(0.1)
        elif data[0] == 49: # Left Blind Right Target
            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            Blind_Flag = 0
            print("→")        
        elif data[0] == 50: # Left Blind Right Noise
            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
            cars.send(command.encode('utf-8'))
            time.sleep(0.1)
            Blind_Flag = 0
            print("↗")
        
    