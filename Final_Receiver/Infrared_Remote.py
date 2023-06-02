'''
Author: Hanqing Qi
Date: 2023-05-31 15:55:24
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 16:19:49
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
port = 122
wlan=None 
s=None

# Temp Counter
Total = 0
Catch = 0

# Send Flag
# NOTE: The flag is a two digit number with the following meaning:
#       Left: first digit | Right: second digit
#       0: no signal      | 0: no signal
#       1: target         | 1: target
#       2: noise          | 2: noise
sendFlag = 00
# Signal
Sig = 0x807f08f7

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
        utime.sleep_ms(90) 
        print("."), # This is just to show that the program is running
        irValueL = recvPinL.my_irread()
        irValueR = recvPinR.my_irread()
        if irValueL:
            print(irValueL)
            if irValueL == hex(Sig):
                sendFlag += 10
                print("Target L")
            else:
                sendFlag += 20
                print("Noise L")
        if irValueR:
            print(irValueR)
            if irValueR == hex(Sig):
                sendFlag += 1
                print("Target R")
            else:
                sendFlag += 2
                print("Noise R")
        if irValueL and irValueR:
            if irValueL == irValueR:
                sendFlag = 11
        if sendFlag != 0:
            Total += 1
            print("sendFlag: ", sendFlag)
        if sendFlag == 11:
            Catch += 1
        # s.send(str(11))
        utime.sleep_ms(110) 
            
# except Exception as e:
except KeyboardInterrupt:
    print("TCP close, please reset!")
    if s:
        s.close()
    wlan.disconnect()
    wlan.active(False)
    print(Total, Catch, Catch/Total)
    # print(e)
    pass