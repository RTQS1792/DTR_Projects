"""
Author       : Hanqing Qi
Date         : 2023-09-29 13:40:04
LastEditors  : Hanqing Qi
LastEditTime : 2023-09-29 13:59:25
FilePath     : /ESP_NOW/Multi_Mac_Address_V1/Serial_Station_PC.py
Description  : 
"""
import serial
import time
import numpy as np

TEST_MESSAGE = "$4#11:11:11:11:11:11#22:22:22:22:22:22#33:33:33:33:33:33#44:44:44:44:44:44$"

class Control_Input:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9
        self.p10 = p10
        self.p11 = p11
        self.p12 = p12
        self.p13 = p13

    def __str__(self) -> str:
        return (
            '<'
            + str(self.p1)
            + '|'
            + str(self.p2)
            + '|'
            + str(self.p3)
            + '|'
            + str(self.p4)
            + '|'
            + str(self.p5)
            + '|'
            + str(self.p6)
            + '|'
            + str(self.p7)
            + '|'
            + str(self.p8)
            + '|'
            + str(self.p9)
            + '|'
            + str(self.p10)
            + '|'
            + str(self.p11)
            + '|'
            + str(self.p12)
            + '|'
            + str(self.p13)
            + '>'
        )


params = []
for i in range(13):
    params.append(np.random.uniform(0, 5))
input = Control_Input(
    params[0],
    params[1],
    params[2],
    params[3],
    params[4],
    params[5],
    params[6],
    params[7],
    params[8],
    params[9],
    params[10],
    params[11],
    params[12],
)

ser = serial.Serial(
    '/dev/cu.wchusbserial1140', 115200
)  # Adjust the COM port and baud rate as necessary

# Print the data and round it to 2 decimal places
# print("Sending data to ESP32: ", input)

message = str(TEST_MESSAGE)
ser.write(message.encode())
try:
    incoming = ser.readline().decode(errors='ignore').strip()
    print("Received Data: " + incoming)
except UnicodeDecodeError:
    print("Received malformed data!")
    
try:
    for i in range(15):
        time.sleep(0.02)
        # NOTE - The daley here need to match the delay in the ESP32 receiver code
        message = str(input)
        ser.write(message.encode())
        # time.sleep(1)
        try:
            incoming = ser.readline().decode(errors='ignore').strip()
            print("Received Data: " + incoming)
        except UnicodeDecodeError:
            print("Received malformed data!")
except KeyboardInterrupt:
    print("Exiting Program")
    ser.close()
