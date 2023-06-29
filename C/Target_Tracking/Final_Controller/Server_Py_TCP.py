'''
Author       : Hanqing Qi
Date         : 2023-06-05 17:48:02
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-08 16:30:35
FilePath     : /Blimps_Team/Final_Controller/Server_Py_TCP.py
Description  : This is the server code for the car using TCP
'''
# echo-server.py
import socket
import time
HOST = "192.168.0.41"  # Standard loopback interface address (localhost)
PORT = 8848  # Port to listen on (non-privileged ports are > 1023)
Flag = 0  # Flag to control the car

IP_ADDRESS = '192.168.0.204'
# cars = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cars.connect((IP_ADDRESS, 5000))
print('Cars connected')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    try:
        while True:
            print("In loop")
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            with conn: 
                print("Waiting for data...")
                while True:
                    data = conn.recv(1)
                    # Make sure the buffer is empty before reading
                    if not data:
                        print("No data")                                
                        break
                    if data:
                        print("Data: ", len(data), data[0])
                        Flag += 1
                        if data[0] == 49:
                            Flag = 0
                            print("Forward")
                            command = 'CMD_MOTOR#1500#1500#1500#1500\n'
                            # cars.send(command.encode('utf-8'))
                            # time.sleep(0.4)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            # cars.send(command.encode('utf-8'))
                        elif data[0] == 48:
                            print("Inrange")
                            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                            # cars.send(command.encode('utf-8'))
                            # time.sleep(0.1)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            # cars.send(command.encode('utf-8'))
                        elif data[0] == 50 and Flag >= 3:
                            print("Searching")
                            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                            # cars.send(command.encode('utf-8'))
                            # time.sleep(0.2)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            # cars.send(command.encode('utf-8'))
            # time.sleep(0.3)
    except:
        command = 'CMD_MOTOR#00#00#00#00\n'
        # cars.send(command.encode('utf-8'))
        print("Closing connection")
        conn.close()