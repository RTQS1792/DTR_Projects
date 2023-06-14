'''
Author       : Hanqing Qi
Date         : 2023-06-01 16:07:56
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-06 17:04:28
FilePath     : /Blimps_Team/Final_Receiver/boot.py
Description  : This is the boot file that let the ESP32 automatically run the code in it's directory
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
        if filename == 'boot.py' or filename == 'irrecvdata.py' or filename == 'data.txt':
            continue
        else:
            print("===============================")
            print(filename,end="")
            if file_type == IS_DIR:
                print(", File is a directory")
                print("===============================")
            else:
                print("\n===============================")
                # print("Contents:")
                # with open(filename) as f:
                #   for line in enumerate(f):
                #       print("{}".format(line[1]),end="")
                # print("")
                exec(open(filename).read(),globals())
    except StopIteration:
        break