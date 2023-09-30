"""
Author       : Hanqing Qi
Date         : 2023-09-29 16:25:39
LastEditors  : Hanqing Qi
LastEditTime : 2023-09-30 17:13:01
FilePath     : /DTR_Projects/ESP_NOW/Multi_Mac_Address_V1/Main.py
Description  : Main for testing ESP-NOW Communication
"""

from Serial_Sender import ESPNOWControl
import time

PORT = "/dev/cu.wchusbserial1140"
LIST_OF_MAC_ADDRESS = [
    "a3:2f:67:b2:45:89",
    "7e:14:c2:9b:d3:56",
    "b0:92:4c:a1:78:e3",
    "5f:13:87:d0:69:72",
    "4a:22:3b:e9:50:61",
]
SLAVE_INDEX = 0
BRODCAST_CHANNEL = 1

if __name__ == "__main__":
    # Initialize the serial connection
    esp_now = ESPNOWControl(PORT, LIST_OF_MAC_ADDRESS)
