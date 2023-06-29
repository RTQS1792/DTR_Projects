'''
Author       : Hanqing Qi
Date         : 2023-06-13 15:25:03
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-15 18:07:31
FilePath     : /undefined/Users/hanqingqi/Library/CloudStorage/Dropbox/Blimps_Team/Rotation_Test_2/control.py
Description  : File to make the vehicle rotation via socket connection
'''

import socket
import time

IP_ADDRESS_1 = '192.168.0.207'
IP_ADDRESS_2 = '192.168.0.204'
snail_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
snail_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
snail_1.connect((IP_ADDRESS_1, 5000))
snail_2.connect((IP_ADDRESS_2, 5000))
print('Cars connected')

try:
    while True:
        command_1 = 'CMD_MOTOR#800#800#-800#-800\n'
        command_2 = 'CMD_MOTOR#900#900#-900#-900\n'
        snail_1.send(command_1.encode('utf-8'))
        snail_2.send(command_2.encode('utf-8'))
        time.sleep(0.1)
except:
    command = 'CMD_MOTOR#00#00#00#00\n'
    snail_1.send(command.encode('utf-8'))
    snail_2.send(command.encode('utf-8'))
    print("Closing connection")
