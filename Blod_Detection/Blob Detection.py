"""
Author       : Hanqing Qi
Date         : 2023-10-06 16:55:08
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-10 18:29:26
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
    (0, 90, -70, 30, -20, 60),  # generic_green_thresholds
    # (0, 40, 0, 50, -100, 0),  # generic_blue_thresholds
]

previous_blobs = []
MIN_CONSISTENT_FRAMES = 1  # for example, adjust as needed

while True:
    clock.tick()
    img = sensor.snapshot()

    current_blobs = []

    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200, merge=True):
        # Check the aspect ratio
        aspect_ratio = blob.w() / blob.h()
        if 0.6 < aspect_ratio < 1.2:
            consistent_frames = 1
            for prev_blob_data in previous_blobs:
                prev_blob = prev_blob_data['blob']
                if abs(blob.cx() - prev_blob.cx()) < 20 and abs(blob.cy() - prev_blob.cy()) < 20:  # 10 pixels tolerance
                    consistent_frames = prev_blob_data['consistent_frames'] + 1
                    break

            current_blobs.append({
                'blob': blob,
                'consistent_frames': consistent_frames
            })

    # Filter blobs based on consistent frames
    for blob_data in current_blobs:
        if blob_data['consistent_frames'] >= MIN_CONSISTENT_FRAMES:
            # Draw the consistent blob
            blob = blob_data['blob']
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

    # Update the previous blobs list for the next frame
    previous_blobs = current_blobs

    print(clock.fps())
