
# Import the library for the IR reciever
from irrecvdata import irGetCMD
import time
from machine import Pin
print("setting led")
led = Pin(2,Pin.OUT)
led.value(0)

print("==============Start of program==============")
recvPinL = irGetCMD(15)  # Left reciever has PIN 15
print("IR receiver online")
Sig = 0xee11ee11

f = open('data.txt', 'a')
f.write('#')

for i in range(150):
    print(i)
    time.sleep(0.2)
    #print("."),
    irValueL = recvPinL.my_irread()
    #print(irValueL)
    if irValueL == hex(Sig):
        #print("1")
        f.write('1')
    else:
        #print("0")
        f.write('0')
# utime.sleep(200)
led.value(1)
time.sleep(1)
#print("led off")
led.value(0)
f.write("#\n")
f.close()