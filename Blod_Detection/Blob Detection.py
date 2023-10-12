"""
Author       : Hanqing Qi
Date         : 2023-10-06 16:55:08
LastEditors  : Hanqing Qi
LastEditTime : 2023-10-12 15:39:17
FilePath     : /Blod_Detection/Blob Detection.py
Description  : Blob Detection Sample Code
"""

import sensor, image, time
from pyb import LED
import mjpeg, pyb
import random
import math

def init_sensor_target(pixformat=sensor.RGB565, framesize=sensor.QVGA, windowsize=None) -> None:
    """
    @description: Initialize the camera sensor for target detection
    @param       {*} pixformat: pixel format - default RGB565
    @param       {*} framesize: frame size - default QVGA (320x240)
    @param       {*} windowsize: window size - default None
    @return      {*} None
    """
    sensor.reset()                        # Initialize the camera sensor.
    sensor.set_pixformat(pixformat)       # Set pixel format to RGB565 (or GRAYSCALE)
    sensor.set_framesize(framesize)       # 160x120 resolution
    if windowsize is not None:            # Set windowing to reduce the resolution of the image
        sensor.set_windowing(windowsize)
    sensor.skip_frames(time=1000)         # Let new settings take affect.
    # sensor.set_auto_exposure(False)
    sensor.set_auto_whitebal(False)
    sensor.__write_reg(0xfe, 0b00000000) # change to registers at page 0
    sensor.__write_reg(0x80, 0b01111100) # enable gamma, CC, edge enhancer, interpolation, de-noise
    sensor.__write_reg(0x81, 0b01100100) # enable BLK dither mode, low light Y stretch, autogray enable
    sensor.__write_reg(0x82, 0b00000100) # enable anti blur, disable AWB
    sensor.__write_reg(0xfe, 0b00000010) # change to registers at page 2
    sensor.__write_reg(0xd1, 0b01100000) # change Cb saturation
    sensor.__write_reg(0xd2, 0b01100000) # change Cr saturation
    sensor.__write_reg(0xd3, 0b01000000) # luma contrast
    sensor.skip_frames(time=2000) # Let the camera adjust.

clock = time.clock()  # Tracks FPS.

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [
    (0, 90, -70, 30, -20, 60),  # generic_green_thresholds
    # (0, 40, 0, 50, -100, 0),  # generic_blue_thresholds
]

init_sensor_target()

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
