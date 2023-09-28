'''
Author: Hanqing Qi
Date: 2023-06-01 15:51:34
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 16:06:00
FilePath: /Blimps_Team/Nework_Test.py
Description: This is the file to test the network connection between ESP32 and PC
'''
import network 
import socket 
import time

ssidRouter = "AIRLab-BigLab"
passwordRouter = "Airlabrocks2022"
host = "192.168.0.41"
port = 80

wlan=None 
s=None

def connectWifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, passwd)

    while wlan.ifconfig()[0] == '0.0.0.0':
        time.sleep(1)
    return True

try:
    connectWifi(ssidRouter, passwordRouter)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host,port))
    print("TCP Connected to:", host, ":", port)
    s.send('Hello')
    s.send('This is my IP.')
    while True:
        s.send('1')

except:
    print("TCP close, please reset!")

    if s:
        s.close()

    wlan.disconnect()
    wlan.active(False)