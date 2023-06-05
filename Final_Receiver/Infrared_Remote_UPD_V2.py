'''
Author       : Hanqing Qi
Date         : 2023-06-02 19:02:40
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-05 18:56:33
FilePath     : /Blimps_Team/Final_Receiver/Infrared_Remote_UPD_V2.py
Description  : This is the main program for the Final Receiver
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
port = 8848
wlan = None
s = None

# Temp Counter
Total = 0
Catch = 0

# Send Flag
sendFlag = 00
# Signal
Sig = 0x807F08F7
# Sig = 0xff30cf


def connectWifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, passwd)

    while wlan.ifconfig()[0] == "0.0.0.0":
        time.sleep(1)
    return True


print("==============Start of program==============")
recvPinL = irGetCMD(15)  # Left reciever has PIN 15
print("Left eye online")
recvPinR = irGetCMD(14)  # Right reciever has PIN 14
print("Right eye online")
try:
    connectWifi(ssidRouter, passwordRouter)

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("UDP Connected to:", host, ":", port)
    print("Listening")
    while True:
        sendFlag = 00
        utime.sleep_ms(200)
        print("."),
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
        # Send the data using UDP
        s.sendto(str(sendFlag).encode(), (host, port))
        # utime.sleep_ms(100)

except KeyboardInterrupt:
    print("UDP close, please reset!")
    if s:
        s.close()
    wlan.disconnect()
    wlan.active(False)
    print(Total, Catch, Catch / Total)
    pass