"""
Author       : Hanqing Qi
Date         : 2023-09-29 16:25:39
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-28 18:14:20
FilePath     : /ESP_NOW/Multi_Mac_Address_V2/Main.py
Description  : Main for testing ESP-NOW Communication
"""

from ESPNOW import ESPNOWControl
import time

PORT = "/dev/cu.wchusbserial1140"
LIST_OF_MAC_ADDRESS = [
    "a3:2f:67:b2:45:89",
    "7e:14:c2:9b:d3:56",
    "b0:92:4c:a1:78:e3",
    "5f:13:87:d0:69:72",
    "4a:22:3b:e9:50:61",
    "34:85:18:91:B5:B4"
]
SLAVE_INDEX = 1
BRODCAST_CHANNEL = 0 # SLAVE_INDEX will override this value if it is not -1
RANDOM_TEST_INPUT = [3.47, 8.92, 0.26, 4.58, 9.14, 7.60, 2.35, 6.84, 5.97, 1.23, 8.50, 0.78, 6.41, 1.11]

if __name__ == "__main__":
    # Initialize the serial connection
    try:
        esp_now = ESPNOWControl(PORT, LIST_OF_MAC_ADDRESS)
        while True:
            esp_now.send(RANDOM_TEST_INPUT, BRODCAST_CHANNEL, SLAVE_INDEX)
            time.sleep(0.1)
            RANDOM_TEST_INPUT = [x + 1 for x in RANDOM_TEST_INPUT]
        # for i in range(5):
        #     for j in range(5):
        #         esp_now.send(RANDOM_TEST_INPUT, BRODCAST_CHANNEL, j)
        #         time.sleep(0.1)
        #     RANDOM_TEST_INPUT = [x + 1 for x in RANDOM_TEST_INPUT]
        # esp_now.close()
    except KeyboardInterrupt:
        esp_now.close()
        print("Program terminated by user")
