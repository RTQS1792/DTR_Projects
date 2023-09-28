# In Memory Basic Frame Differencing Example
#
# This example demonstrates using frame differencing with your OpenMV Cam. It's
# called basic frame differencing because there's no background image update.
# So, as time passes the background image may change resulting in issues.

import math
import sensor, image, time, pyb, omv, os
import image, network, rpc, struct, tf
from pyb import UART

from machine import Pin, Signal

#---- Global Variables ----#
INFRARED_LED_PIN = "PC4"
GOAL_COLOR_THRESHOLD = (0, 100, -30, 30, -30, 30)


TRIGGER_THRESHOLD = 5


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def one_norm_dist(v1, v2):
    return sum([abs(v1[i] - v2[i]) for i in range(len(v1))])


def two_norm_dist(v1, v2):
    return math.sqrt(sum([(v1[i] - v2[i]) ** 2 for i in range(len(v1))]))


class TrackedRect:
    def __init__(
        self,
        init_rect,
        norm_level: int,
        feature_dist_threshold=300,
        untracked_frame_threshold=20,
    ):
        self.feature_vec = []
        for i in range(4):
            for j in range(2):
                self.feature_vec.append(init_rect.corners()[i][j])
        self.norm_level = norm_level
        self.untracked_frames = 0
        self.feature_dist_threshold = feature_dist_threshold
        self.untracked_frame_threshold = untracked_frame_threshold
        # print("new rectangle")

    def update(self, rects):
        min_dist = 32767
        candidate_feature = None
        for r in rects:
            # calculate new feature vector
            bad_rect = False
            for x in range(4):
                if r.corners()[x][0] == 0 and r.corners()[x][1] == 0:
                    bad_rect = True
            if not bad_rect:
                feature_vec = []
                for i in range(4):
                    for j in range(2):
                        feature_vec.append(r.corners()[i][j])
                if self.norm_level == 1:
                    dist = one_norm_dist(self.feature_vec, feature_vec)
                elif self.norm_level == 2:
                    dist = two_norm_dist(self.feature_vec, feature_vec)
                else:
                    # we do not need any other norm now
                    assert False
                if dist < min_dist:
                    min_dist = dist
                    candidate_feature = feature_vec
        if min_dist < self.feature_dist_threshold:
            self.feature_vec = candidate_feature
            self.untracked_frames = 0
            # print("replaced! {}".format(min_dist))
            # still valid
            return True
        else:
            self.untracked_frames += 1
            # print("Dropped? {}".format(min_dist))
            if self.untracked_frames >= self.untracked_frame_threshold:
                # invalid rectangle now
                return False
        return True


ondiff = 3000
slow_led = False


def difference_goal_rect(
    clock,
    time_start,
    led_pin,
    extra_fb=None,
    tracked_rect=None,
    show=True,
):
    clock.tick()  # Track elapsed milliseconds between snapshots().
    omv.disable_fb(True)
    elapsed = 21000 - (int((time.time_ns() - time_start) / 1000))
    if elapsed > 0:
        time.sleep_us(elapsed)
    extra_fb = sensor.alloc_extra_fb(
        sensor.width(), sensor.height(), sensor.RGB565
    )
    extra_fb.replace(sensor.snapshot())
    time_start = time.time_ns()
    led_pin.value(0)
    elapsed = 20000 - (int((time.time_ns() - time_start) / 1000))
    if elapsed > 0:
        if elapsed > 3000:
            time.sleep_us(elapsed - 3000)
            time.sleep_us(3000)
        else:
            time.sleep_us(elapsed)
    img = sensor.snapshot()  # Take a picture and return the image.
    led_pin.value(1)
    time_start = time.time_ns()
    img.sub(extra_fb, reverse=True)
    sensor.dealloc_extra_fb()
    img.lens_corr(1.65)
    img.negate()

    # Find color blobs.
    blobs = img.find_blobs([GOAL_COLOR_THRESHOLD], area_threshold=0,
                   pixels_threshold=0,
                   margin = 15)

    for blob in blobs:
        if blob.elongation() > 0.5:  # Adjust this threshold as needed.
            draw_rectangle(img, blob)

    omv.disable_fb(False)
    return time_start, tracked_rect

def draw_rectangle(img, blob):
    img.draw_rectangle(blob.rect(), color=(0, 255, 0))
    # img.flush()

def init_sensor_goal() -> None:
    """
    description: Initializes the sensor for goal detection
    return      {*}: None
    """
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time=1000)
    sensor.set_auto_whitebal(False)
    sensor.set_auto_exposure(False, exposure_us=10000)
    sensor.set_contrast(-3)
    sensor.set_saturation(3)
    sensor.set_brightness(3)
    sensor.skip_frames(time=1000)

def init_sensor_target() -> None:
    """
    description: Initializes the sensor for target detection
    return      {*}: None
    """
    sensor.reset()  # Reset and initialize the sensor.
    sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
    # sensor.set_windowing((240, 240))       # Set 240x240 window.
    sensor.set_auto_exposure(False)
    sensor.set_auto_whitebal(False)
    sensor.__write_reg(0xFE, 0b00000000)  # change to registers at page 0
    print(sensor.__read_reg(0x80))
    sensor.__write_reg(0x03, 0b00000000)  # high bits of exposure control
    sensor.__write_reg(0x04, 0b11100000)  # low bits of exposure control
    sensor.__write_reg(0xB0, 0b01110000)  # global gain
    sensor.__write_reg(0xAD, 0b01110000)  # R ratio
    sensor.__write_reg(0xAE, 0b01110000)  # G ratio
    sensor.__write_reg(0xAF, 0b01110100)  # B ratio
    # RGB gains
    sensor.__write_reg(0xA3, 0b10001010)  # G gain odd
    sensor.__write_reg(0xA4, 0b10001010)  # G gain even
    sensor.__write_reg(0xA5, 0b10000000)  # R gain odd
    sensor.__write_reg(0xA6, 0b10000000)  # R gain even
    sensor.__write_reg(0xA7, 0b10010000)  # B gain odd
    sensor.__write_reg(0xA8, 0b10010000)  # B gain even
    sensor.__write_reg(0xA9, 0b10000000)  # G gain odd 2
    sensor.__write_reg(0xAA, 0b10000000)  # G gain even 2

    sensor.__write_reg(0xFE, 0b00000010)  # change to registers at page 2
    # sensor.__write_reg(0xd0, 0b00000000)   # change global saturation,
    # strangely constrained by auto saturation
    sensor.__write_reg(0xD1, 0b01110000)  # change Cb saturation
    sensor.__write_reg(0xD2, 0b01100000)  # change Cr saturation
    sensor.__write_reg(0xD3, 0b01000000)  # luma contrast
    sensor.__write_reg(0xD5, 0b00000000)  # luma offset
    sensor.skip_frames(time=2000)  # Let the camera adjust.


if __name__ == "__main__":
    show = True

    framesize = sensor.QVGA
    quick = True
    extra_fb = None

    # Define the leds
    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    blue_led = pyb.LED(3)

    time_start = time.time_ns()
    tracked_rect = None

    flag_last = time.time_ns()

    flag = 1
    while True:
        if flag == 0:  # nueral network
            init_sensor_target()  # Initialize the sensor for target tracking
        elif flag == 1:  # goal detection
            init_sensor_goal()  # Initialize the sensor for goal tracking
            clock = time.clock()  # Tracks FPS.
            led_pin = Pin(INFRARED_LED_PIN, Pin.OUT) # Define the infrared led pin
            time_start, tracked_rect = difference_goal_rect(
                clock, time_start, led_pin, extra_fb, tracked_rect, show
            )
        elif flag == 2:  # Fully autonoomous
            pass
            # TODO: Add fully autonomous code
        else:  # Not a valid flag
            pass
