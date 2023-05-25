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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    try:
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            with conn: 
                print("Waiting for data...")
                while True:       
                    data = conn.recv(1)
                    # Make sure the buffer is empty before reading
                    if not data:
                        break
                    if data:
                        print("Data: ", len(data), data[0])
            time.sleep(0.5)
    except:
        print("Closing connection")
        conn.close()