"""
Author       : Hanqing Qi
Date         : 2023-10-06 16:17:30
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-06 16:34:05
FilePath     : /Blod_Detection/Camera Calibrate.py
Description  : Sample code for camera calibration
"""

import sensor, image, time
from pyb import LED
import mjpeg, pyb
import random

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)

sensor.set_auto_exposure(False)
sensor.set_auto_whitebal(False)
sensor.__write_reg(0xFE, 0b00000000)  # change to registers at page 0
sensor.__write_reg(0x03, 0b00000001)  # high bits of exposure control
sensor.__write_reg(0x04, 0b11111000)  # low bits of exposure control
sensor.__write_reg(0xB0, 0b01111000)  # global gain
sensor.__write_reg(0xAD, 0b01110000)  # R ratio
sensor.__write_reg(0xAE, 0b01100000)  # G ratio
sensor.__write_reg(0xAF, 0b10001101)  # B ratio
### RGB gains
sensor.__write_reg(0xA3, 0b10001010)  # G gain odd
sensor.__write_reg(0xA4, 0b10001010)  # G gain even
sensor.__write_reg(0xA5, 0b10000000)  # R gain odd
sensor.__write_reg(0xA6, 0b10000000)  # R gain even
sensor.__write_reg(0xA7, 0b10010000)  # B gain odd
sensor.__write_reg(0xA8, 0b10010000)  # B gain even
sensor.__write_reg(0xA9, 0b10000000)  # G gain odd 2
sensor.__write_reg(0xAA, 0b10000000)  # G gain even 2

sensor.__write_reg(0xFE, 0b00000010)  # change to registers at page 2
sensor.__write_reg(0xD1, 0b01110000)  # change Cb saturation
sensor.__write_reg(0xD2, 0b01111000)  # change Cr saturation
sensor.__write_reg(0xD3, 0b01000000)  # luma contrast
sensor.__write_reg(0xD5, 0b00000000)  # luma offset

clock = time.clock()  # Tracks FPS.

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  
    # NOTE: OpenMV Cam runs about half as fast when connected to the IDE. The FPS should increase once disconnected.
