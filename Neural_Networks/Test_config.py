# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time

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
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
