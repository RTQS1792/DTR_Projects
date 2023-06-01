'''
Author: Hanqing Qi
Date: 2023-05-31 15:55:24
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 15:14:00
FilePath: /Blimps_Team/Python/Infrared_Reciever/boot.py
Description: The is just the boot file that will let the board run all the python files in it's directory
'''
#!/opt/bin/lv_micropython
import uos as os
import uerrno as errno
iter = os.ilistdir()
IS_DIR = 0x4000
IS_REGULAR = 0x8000

while True:
    try:
        entry = next(iter)
        filename = entry[0]
        file_type = entry[1]
        # Skip the ireecvdata.py since this is the library file for the IR reciever
        if filename == 'boot.py' or 'irrecvdata.py':
            continue
        else:
            print("===============================")
            print(filename,end="")
            if file_type == IS_DIR:
                print(", File is a directory")
                print("===============================")
            else:
                print("\n===============================")
                #print("Contents:")
                #with open(filename) as f:
                #   for line in enumerate(f):
                #       print("{}".format(line[1]),end="")
                #print("")
                exec(open(filename).read(),globals())
    except StopIteration:
        break