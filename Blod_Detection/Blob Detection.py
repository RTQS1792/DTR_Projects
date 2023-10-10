"""
Author       : Hanqing Qi
Date         : 2023-10-06 16:55:08
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-06 16:58:55
FilePath     : /Blod_Detection/Blob Detection.py
Description  : Blob Detection Sample Code
"""

import sensor, image, time
from pyb import LED
import mjpeg, pyb
import random
import math

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

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [
    (30, 80, -50, -10, 10, 50),  # generic_green_thresholds
    # (0, 40, 0, 50, -100, 0),  # generic_blue_thresholds
]

while True:
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() < 0.5:
            # These values are stable all the time.
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            # Note - the blob rotation is unique to 0-180 only.
            img.draw_keypoints(
                [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
            )
    print(clock.fps())
