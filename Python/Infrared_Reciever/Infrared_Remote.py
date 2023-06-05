'''
Author: Hanqing Qi
Date: 2023-05-31 15:55:24
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 15:19:23
FilePath: /Blimps_Team/Python/Infrared_Reciever/Infrared_Remote.py
Description: This is the infrared reciever file that will be used to recieve the IR signal from the remote
'''
from irrecvdata import irGetCMD
import utime

print("==============Start of program==============")
recvPinL = irGetCMD(15) # Left reciever has PIN 15
print("Left eye online")
recvPinR = irGetCMD(14) # Right reciever has PIN 14
print("Right eye online")
try:
    print("Listening")
    while True:
        utime.sleep_ms(100) 
        print("."), # This is just to show that the program is running
        irValueL = recvPinL.my_irread()
        irValueR = recvPinR.my_irread()
        if irValueL:
            print("Left: ", irValueL)
        if irValueR:
            print("Right: ", irValueR)
except Exception as e:
    print(e)
    pass

        











