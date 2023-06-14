'''
Author       : Hanqing Qi
Date         : 2023-06-13 15:25:03
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-13 17:46:19
FilePath     : /Blimps_Team/Python/Rotation_Test/control.py
Description  : File to make the vehicle rotation via socket connection
'''

import socket
import time

IP_ADDRESS = '192.168.0.207'
cars = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cars.connect((IP_ADDRESS, 5000))
print('Cars connected')

try:
    while True:
        command = 'CMD_MOTOR#650#650#-650#-650\n'
        cars.send(command.encode('utf-8'))
        time.sleep(0.1)
except:
    command = 'CMD_MOTOR#00#00#00#00\n'
    cars.send(command.encode('utf-8'))
    print("Closing connection")
