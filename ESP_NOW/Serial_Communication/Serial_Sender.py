'''
Author       : Hanqing Qi
Date         : 2023-07-20 13:34:09
LastEditors  : Hanqing Qi
LastEditTime : 2023-07-21 14:25:14
FilePath     : /ESP_NOW/Serial_Communication/Serial_Sender.py
Description  : Sender to send data to ESP32 through hardware serial port
'''
import serial
import time

ser = serial.Serial('/dev/cu.wchusbserial2140', 115200)  # Adjust the COM port and baud rate as necessary

try:
    for i in range(180):
        time.sleep(0.05)
        # NOTE - The daley here need to match the delay in the ESP32 receiver code
        message = str(i)
        ser.write(message.encode())
        # time.sleep(1)
        incoming = ser.readline().decode().strip()
        print("Received from ESP32: ", incoming)
except KeyboardInterrupt:
    print("Exiting Program")
    ser.close()