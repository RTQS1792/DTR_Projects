'''
Author: Hanqing Qi
Date: 2023-05-31 15:55:24
LastEditors: Hanqing Qi
LastEditTime: 2023-06-01 15:27:15
FilePath: /Blimps_Team/Python/Infrared_Reciever/irrecvdata.py
Description: This is the library file for the IR reciever
'''
import machine
import utime
import micropython

class irGetCMD(object):
    '''
    description: Class constructor
    param {*} self
    param {*} gpioNum
    return {*}
    '''    
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

    '''
    description: This is the interrupt handler for the IR reciever. It will be called when the IR reciever detects a change in the signal
    param {*} self
    param {*} source
    return {*}
    '''    
    def __logHandler(self, source):
        thisComeInTime = utime.ticks_us()
        if self.start == 0:
            self.start = thisComeInTime
            self.index = 0
            return
        self.logList.append(utime.ticks_diff(thisComeInTime, self.start)) # This is the time difference between the two changes of the signal
        self.start = thisComeInTime 
        self.index += 1 # This is the index for the logList
    
    '''
    description: This is the modified function that is used to read the signal sending using the NEC protocol.
    param {*} self
    return {*} irValue: This is the decoded value of the signal
    '''    
    def my_irread(self):
        # We want to make sure the clicking rate is less than 10 Hz, or the signal is not valid
        if utime.ticks_diff(
                utime.ticks_us(),
                self.start) > 100000 and self.index > 0:
            ir_buffer=[] # This is the buffer for the signal
            # If the signal length is less than 66, then it is not valid
            if len(self.logList) < 66:
                return None
            # Decode the 32 bits signal, we only care about the peak thus we only need to check the odd index
            for i in range(3,66,2):
                if self.logList[i]>560:
                    ir_buffer.append(1)
                else:
                    ir_buffer.append(0)
                                
            # Buffer for the decoded value  
            irValue=0x00000000
            for i in range(0,4):
                for j in range(0,8):
                    # If the bit is 1, then we shift the value to the left and add 1
                    if ir_buffer[i*8+j]==1:
                        irValue=irValue<<1
                        irValue |= 0x01
                    # If the bit is 0, then we shift the value to the left and add 0
                    else:
                        irValue=irValue<<1
                        irValue &= 0xfffffffe                    
            # Reset the logList and index
            self.logList = []
            self.index = 0
            self.start = 0
            return hex(irValue)
        
    '''
    description: This is the default function that is used to read the signal sending with the remote controller in the ESP32 kit.
    param {*} self
    return {*}
    '''    
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