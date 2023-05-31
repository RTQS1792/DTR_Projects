import machine
import utime
import micropython

class irGetCMD(object):
    def __init__(self, gpioNum):
        self.irRecv = machine.Pin(gpioNum, machine.Pin.IN, machine.Pin.PULL_UP)
        self.irRecv.irq(
            trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
            handler=self.__logHandler)
        self.logList = []
        self.index = 0
        self.start = 0
        self.dictKeyNum = 0
        self.irDict = {}

    def __logHandler(self, source):
        thisComeInTime = utime.ticks_us()
        if self.start == 0:
            self.start = thisComeInTime
            self.index = 0
            return
        self.logList.append(utime.ticks_diff(thisComeInTime, self.start))
        self.start = thisComeInTime
        self.index += 1
    
    # The new IR read that *might* work with ARduino IRsend
    def my_irread(self):
        # utime.sleep_ms(100)
        # We want to make sure the clicking rate is less than 10 Hz
        if utime.ticks_diff(
                utime.ticks_us(),
                self.start) > 100000 and self.index > 0:
            ir_buffer=[]
            #print("2")
            if len(self.logList) < 66:
                return None
            
            # print(len(self.logList))
            for i in range(3,66,2):
                # print(self.logList[i])
                if self.logList[i]>560:
                    ir_buffer.append(1)
                else:
                    ir_buffer.append(0)
                                
            # buffer for real data        
            irValue=0x00000000
            # print("4")
            for i in range(0,4):
                for j in range(0,8):
                    # print("4")
                    if ir_buffer[i*8+j]==1:
                        irValue=irValue<<1
                        irValue |= 0x01
                    else:
                        irValue=irValue<<1
                        irValue &= 0xfffffffe                    
            # reset 
            self.logList = []
            self.index = 0
            self.start = 0
            return hex(irValue)
        
    def ir_read(self):
        utime.sleep_ms(100) 
        if utime.ticks_diff(
                utime.ticks_us(),
                self.start) > 800000 and self.index > 0:
            ir_buffer=[]
            #print("2")
            if len(self.logList) < 32:
                return 0x00000
            for i in range(3,66,2):
                # print("3")
                if self.logList[i]>800:
                    ir_buffer.append(1)
                else:
                    ir_buffer.append(0)
            irValue=0x00000000
            for i in range(0,4):
                for j in range(0,8):
                    # print("4")
                    if ir_buffer[i*8+j]==1:
                        irValue=irValue<<1
                        irValue |= 0x01
                    else:
                        irValue=irValue<<1
                        irValue &= 0xfffffffe                    
            # reset 
            self.logList = []
            self.index = 0
            self.start = 0
            return hex(irValue)