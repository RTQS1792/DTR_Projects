# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time
from pyb import LED
import mjpeg, pyb
import random

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.set_auto_exposure(False)
sensor.__write_reg(0xfe, 0b00000000) # change to registers at page 0
print(sensor.__read_reg(0x80))
sensor.__write_reg(0x03, 0b00000000) # high bits of exposure control
sensor.__write_reg(0x04, 0b01001000) # low bits of exposure control
sensor.__write_reg(0xb0, 0b01110000) # global gain
sensor.__write_reg(0xad, 0b01011000) # R ratio
sensor.__write_reg(0xae, 0b01100000) # G ratio
sensor.__write_reg(0xaf, 0b10000100) # B ratio
sensor.__write_reg(0xfe, 0b00000010) # change to registers at page 2
sensor.__write_reg(0xd1, 0b01110000) # change Cb saturation
sensor.__write_reg(0xd2, 0b01100000) # change Cr saturation
sensor.set_auto_whitebal(False)
#sensor.set_auto_gain(False, 0.0)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

num_frames = 2000

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)
clock = time.clock() # Tracks FPS.

# start = pyb.millis()
m = mjpeg.Mjpeg("data_highbay_{}.mjpeg".format(random.randint(0, 100000)))
i = 0
while i < num_frames:

    green_led.on()
    clock.tick()
    m.add_frame(sensor.snapshot())
    print(clock.fps())
    green_led.off()
    i += 1

m.close(clock.fps())

while True:
    pass
