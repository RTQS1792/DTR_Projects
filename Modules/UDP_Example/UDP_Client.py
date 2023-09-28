'''
Author: Hanqing Qi
Date: 2023-06-02 16:24:58
LastEditors: Hanqing Qi
LastEditTime: 2023-06-02 17:03:14
FilePath: /Blimps_Team/Python/UDP_Example/UDP_Client.py
Description: This is the file to test the UDP connection between ESP32 and PC
'''
import socket
import network
import time

ssidRouter = "AIRLab-BigLab"
passwordRouter = "Airlabrocks2022"
host = "192.168.0.41"
port = 8848

def udp_example():
    # Set up network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssidRouter, passwordRouter)

    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())

    # Set up UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    server_address = (host, port)
    message = b'This is the message.'
    
    try:
        while True:
            # Send data
            print('sending {!r}'.format(message))
            sent = sock.sendto(message, server_address)
            time.sleep(1)
            # break
            # Receive response
            # print('waiting to receive')
            # data, server = sock.recvfrom(4096)
            # print('received {!r}'.format(data))

    finally:
        print('closing socket')
        # station.active(False)
        sock.close()

udp_example()