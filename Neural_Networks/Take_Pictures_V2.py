# Untitled - By: hanqingqi - Mon Jul 24 2023
import sensor, image, pyb


def init_sensor(
    pixformat=sensor.RGB565,
    framesize=sensor.HQVGA,
    windowsize=None,
    gain=18,
    autoexposure=False,
    exposure=10000,
    autowhitebal=False,
    white_balance=(0, 0, 0),
    contrast=0,
    saturation=0,
):
    '''
    description: Initialize the camera sensor
    param       {*} pixformat: RGB565, GRAYSCALE, JPEG
    param       {*} framesize: QQVGA, HQVGA, QVGA, VGA, SVGA, SXGA, UXGA
    param       {*} windowsize: (x, y, w, h)
    param       {*} gain: The sensitivity of the camera sensor to light
    param       {*} autoexposure: Whether to automatically adjust the exposure time
    param       {*} exposure: Exposure time
    param       {*} autowhitebal: Whether to automatically adjust the white balance
    param       {*} white_balance: White balance 3-tuple (red, green, blue)
    param       {*} contrast: Contrast from -3 to 3
    param       {*} saturation: Saturation from -3 to 3
    return      {*} None
    '''
    sensor.reset()
    sensor.set_pixformat(pixformat)
    sensor.set_framesize(framesize)
    if windowsize:
        sensor.set_windowing(windowsize)
    sensor.skip_frames(time=1000)
    sensor.set_auto_gain(False, gain_db=gain)
    sensor.set_auto_whitebal(autowhitebal, rgb_gain_db=white_balance)
    sensor.set_auto_whitebal(True)
    sensor.set_auto_exposure(autoexposure, exposure_us=exposure)
    sensor.set_contrast(contrast)
    sensor.set_saturation(saturation)
    sensor.skip_frames(time=1000)
    sensor.__write_reg(0x0E, 0b00000000)
    sensor.__write_reg(0x3E, 0b00000000)
    sensor.skip_frames(time=1000)


init_sensor(
    pixformat=sensor.RGB565,
    framesize=sensor.QVGA,
    windowsize=None,
    gain=6,
    autoexposure=False,
    exposure=5000,
    autowhitebal=False,
    white_balance=(-6.02073, -5.49487, -1.804),
    contrast=-3,
    saturation=0,
)

i = 0
while True:
    i += 1
    sensor.skip_frames(time=200)  # Give the user time to get ready.
    print("You're on camera! pic " + str(i))
    sensor.snapshot().save("image" + str(i) + ".jpg")  # or "example.bmp" (or others)
    # sensor.skip_frames(time = 500) # Give the user time to get ready.
    print("Done")
