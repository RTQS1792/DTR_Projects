# echo-server.py
'''
Author: Hanqing Qi
Date: 05/25/2023 
Description: This is the server that listen to ESP32.
'''
import socket
import time
HOST = "192.168.0.41"  # Standard loopback interface address (localhost)
PORT = 80  # Port to listen on (non-privileged ports are > 1023)
Flag = 0  # Flag to control the car

IP_ADDRESS = '192.168.0.204'
cars = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cars.connect((IP_ADDRESS, 5000))
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
                    Flag += 1
                    if Flag >= 3:
                        command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                        cars.send(command.encode('utf-8'))
                        time.sleep(0.2)
                        command = 'CMD_MOTOR#00#00#00#00\n'
                        cars.send(command.encode('utf-8'))       
                    print("Where is the data?")
                    data = conn.recv(1)
                    # Make sure the buffer is empty before reading
                    if not data:
                        print("No data")                                
                        break
                    if data:
                        Flag = 0
                        print("Data: ", len(data), data[0])
                        if data[0] == 49:
                            print("Forward")
                            command = 'CMD_MOTOR#1500#1500#1500#1500\n'
                            cars.send(command.encode('utf-8'))
                            time.sleep(0.4)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            cars.send(command.encode('utf-8'))
                        elif data[0] == 48:
                            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                            cars.send(command.encode('utf-8'))
                            time.sleep(0.1)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            cars.send(command.encode('utf-8'))
                        else:
                            command = 'CMD_MOTOR#1100#1100#-1100#-1100\n'
                            cars.send(command.encode('utf-8'))
                            time.sleep(0.2)
                            command = 'CMD_MOTOR#00#00#00#00\n'
                            cars.send(command.encode('utf-8'))
            time.sleep(0.5)
    except:
        command = 'CMD_MOTOR#00#00#00#00\n'
        cars.send(command.encode('utf-8'))
        print("Closing connection")
        conn.close()