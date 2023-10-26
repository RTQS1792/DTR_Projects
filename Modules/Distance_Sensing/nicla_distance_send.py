"""
Author       : Hanqing Qi
Date         : 2023-10-20 17:16:42
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-20 17:16:43
FilePath     : /Distance_Sensing/nicla_distance_send.py
Description  : Send the distance data to the esp32
"""

from machine import I2C
from vl53l1x import VL53L1X
from pyb import UART
import time

# Initialize ToF sensor
tof = VL53L1X(I2C(2))

def read_distance():
    """
    Continuously reads and prints distance from ToF sensor.
    """
    while True:
        try:
            distance = tof.read()
        except:
            distance = 9999  # Large value to indicate error
        print(f"Distance: {distance}mm")
        time.sleep_ms(20)

def checksum(arr, initial=0):
    """
    Calculates the checksum for a given array.
    """
    sum = initial
    for a in arr:
        sum += a
    checksum = 0xFFFF - sum
    chA = checksum >> 8
    chB = checksum & 0xFF
    return chA, chB

def send_distance():
    """
    Reads distance from ToF sensor and sends it over UART after packaging with checksum.
    """
    # Set up UART (use appropriate settings for your board)
    uart = UART("LP1", 115200, timeout_char=2000) # (TX, RX) = (P1, P0) = (PB14, PB15)
    while True:
        try:
            distance = tof.read()
        except:
            distance = 9999  # Large value to indicate error

        btdistance = bytearray(distance.to_bytes(2, 'little'))

        # Prepare message to send
        msg = bytearray([0x20, 0x40] + list(btdistance) + [0x00] * (30 - len(btdistance)))

        # Calculate and append checksum
        chA, chB = checksum(msg[:-2], 0)
        msg[-1] = chA
        msg[-2] = chB

        # Print the message in one line
        print("Sending: ", end="")
        for i in msg:
            print(i, end=" ")
        print("DONE")
        uart.write(msg)
        time.sleep(1)

if __name__ == "__main__":
    # Uncomment based on your requirement
    # read_distance()
    send_distance()

