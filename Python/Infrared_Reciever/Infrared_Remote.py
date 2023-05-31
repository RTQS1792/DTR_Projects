from irrecvdata import irGetCMD
import utime


print("==============Start of program==============")
recvPinL = irGetCMD(15)
print("Left eye online")
recvPinR = irGetCMD(14)
print("Right eye online")
try:
    print("Listening")
    while True:
        utime.sleep_ms(100) 
        print(".")
        irValueL = recvPinL.my_irread()
        irValueR = recvPinR.my_irread()
        if irValueL:
            print("Right: ", irValueL)
        if irValueR:
            print("Left: ", irValueR)
except Exception as e:
    print(e)
    pass

        











