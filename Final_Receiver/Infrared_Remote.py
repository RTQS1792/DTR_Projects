'''
Author: Hanqing Qi
Date: 2023-05-31 15:55:24
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 16:14:43
FilePath: /Blimps_Team/Final_Receiver/Infrared_Remote.py
Description: This is the infrared reciever file that will be used to recieve the IR signal from the remote
'''
# Import the library for the IR reciever
from irrecvdata import irGetCMD
import utime
# Import the library for the network connection
import network 
import socket 
import time

# Variables for the network connection
ssidRouter = "AIRLab-BigLab"
passwordRouter = "Airlabrocks2022"
host = "192.168.0.41"
port = 80
wlan=None 
s=None

# Send Flag
# NOTE: The flag is a two digit number with the following meaning:
#       Left: first digit | Right: second digit
#       0: no signal      | 0: no signal
#       1: target         | 1: target
#       2: noise          | 2: noise
sendFlag = 00

'''
description: This function is used to connect the ESP32 to the router
param {*} ssid
param {*} passwd
return {*} True if the connection is successful
'''
def connectWifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, passwd)

    while wlan.ifconfig()[0] == '0.0.0.0':
        time.sleep(1)
    return True

print("==============Start of program==============")
recvPinL = irGetCMD(15) # Left reciever has PIN 15
print("Left eye online")
recvPinR = irGetCMD(14) # Right reciever has PIN 14
print("Right eye online")
try:
    # Connect to the router
    connectWifi(ssidRouter, passwordRouter)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host,port))
    print("TCP Connected to:", host, ":", port)
    # Start the reciever
    print("Listening")
    while True:
        sendFlag = 00 # Reset the sendFlag
        utime.sleep_ms(100) 
        print("."), # This is just to show that the program is running
        irValueL = recvPinL.my_irread()
        irValueR = recvPinR.my_irread()
        if irValueL:
            print("Left: ", irValueL)
        if irValueR:
            print("Right: ", irValueR)
            
except Exception as e:
    print("TCP close, please reset!")
    if s:
        s.close()
    wlan.disconnect()
    wlan.active(False)
    print(e)
    pass

        











