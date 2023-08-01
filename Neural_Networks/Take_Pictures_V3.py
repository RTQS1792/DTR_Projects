# Snapshot Example
#
# Note: You will need an SD card to run this example.
#
# You can use your OpenMV Cam to save image files.

import sensor, image, pyb, time

RED_LED_PIN = 1
BLUE_LED_PIN = 3
from pyb import Pin


sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA)# or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
pin7 = Pin('P7', Pin.OUT_PP, Pin.PULL_NONE)

i = 0
#pin7.value(False)
while(True):

    i += 1

    pyb.LED(RED_LED_PIN).on()
    #sensor.skip_frames(time = 1000) # Give the user time to get ready.
    time.sleep_ms(50)
    pyb.LED(RED_LED_PIN).off()
    pyb.LED(BLUE_LED_PIN).on()
    #f i % 2:
    pin7.value(True)
    #else:
    #    pin7.value(False)



    print("You're on camera! pic "+str(i))
    sensor.snapshot().save("image"+str(i)+".jpg") # or "example.bmp" (or others)

   # sensor.skip_frames(time = 1000) # Give the user time to get ready.

    pyb.LED(BLUE_LED_PIN).off()
    print("Done! Reset the camera to see the saved image.")
