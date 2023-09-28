import math
import sensor, image, time, pyb, omv, os
import image, network, rpc, struct, tf
from pyb import UART
from machine import Pin, Signal
pink_threshold = (15, 70, 10, 60, -20, 15)
lab_thresh_tool = (0, 93, -63, 5, -128, 127)
green_threshold = (65, 80, -35, 10, 35, 70)
orange_threshold = (52, 65, 55, 75, 30, 50)
wide_thresh_hand = (75, 93, -40, 0, 0, 65)
green_thresh_hand  = (23,75,-25,0,0,20)
TRIGGER_THRESHOLD = 5
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
def one_norm_dist(v1, v2):
    return sum([abs(v1[i] - v2[i]) for i in range(len(v1))])
def two_norm_dist(v1, v2):
    return math.sqrt(sum([(v1[i] - v2[i])**2 for i in range(len(v1))]))
class TrackedBlob:
    def __init__(self, init_blob, norm_level: int,
                       feature_dist_threshold=300,
                       window_size = 5):
        self.blob_history = [init_blob]
        self.feature_vector = [init_blob.x(),
                               init_blob.y(),
                               init_blob.w(),
                               init_blob.h(),
                               init_blob.rotation_deg()]
        self.norm_level = norm_level
        self.untracked_frames = 0
        self.feature_dist_threshold = feature_dist_threshold
        self.window_size = window_size
    def compare(self, new_blob):
        feature = (new_blob.x(),
                   new_blob.y(),
                   new_blob.w(),
                   new_blob.h(),
                   new_blob.rotation_deg())
        my_feature = self.feature_vector
        if not new_blob.code() == self.blob_history[-1].code():
            return 32767
        elif self.norm_level == 1:
            return (math.fabs(feature[0]-my_feature[0]) +
                    math.fabs(feature[1]-my_feature[1]) +
                    math.fabs(feature[2]-my_feature[2]) +
                    math.fabs(feature[3]-my_feature[3]) +
                    math.fabs(feature[4]-my_feature[4]))
        else:
            return math.sqrt((feature[0]-my_feature[0])**2 +
                             (feature[1]-my_feature[1])**2 +
                             (feature[2]-my_feature[2])**2 +
                             (feature[3]-my_feature[3])**2 +
                             (feature[4]-my_feature[4])**2)
    def update(self, blobs):
        if blobs is None:
            self.untracked_frames += 1
            return False
        min_dist = 32767
        candidate_blob = None
        for b in blobs:
            dist = self.compare(b)
            if dist < min_dist:
                min_dist = dist
                candidate_blob = b
        if min_dist < self.feature_dist_threshold:
            history_size = len(self.blob_history)
            self.blob_history.append(candidate_blob)
            feature = (candidate_blob.x(),
                       candidate_blob.y(),
                       candidate_blob.w(),
                       candidate_blob.h(),
                       candidate_blob.rotation_deg())
            if history_size <  self.window_size:
                for i in range(5):
                    self.feature_vector[i] = (self.feature_vector[i]*history_size +
                        feature[i])/(history_size + 1)
                self.untracked_frames = 0
                print("replaced! {}".format(min_dist))
            else:
                oldest_blob = self.blob_history[0]
                oldest_feature = (oldest_blob.x(),
                                  oldest_blob.y(),
                                  oldest_blob.w(),
                                  oldest_blob.h(),
                                  oldest_blob.rotation_deg())
                for i in range(5):
                    self.feature_vector[i] = (self.feature_vector[i]*self.window_size +
                        feature[i] - oldest_feature[i])/self.window_size
                self.blob_history.pop(0)
            return True
        else:
            self.untracked_frames += 1
            return False
class TrackedRect2:
    def __init__(self, init_rect, norm_level: int,
                       feature_dist_threshold=300,
                       window_size = 5):
        self.rect_history = [init_rect]
        self.feature_vector = []
        for i in range(4):
            for j in range(2):
                self.feature_vector.append(init_rect.corners()[i][j])
        self.norm_level = norm_level
        self.untracked_frames = 0
        self.feature_dist_threshold = feature_dist_threshold
        self.window_size = window_size
    def compare(self, new_rect):
        feature = []
        for i in range(4):
            for j in range(2):
                feature.append(new_rect.corners()[i][j])
        my_feature = self.feature_vector
        if self.norm_level == 1:
            dist = one_norm_dist(self.feature_vector, feature)
        elif self.norm_level == 2:
            dist = two_norm_dist(self.feature_vector, feature)
        else:
            assert(False)
        return dist
    def update(self, rects):
        if rects is None:
            self.untracked_frames += 1
            return False
        min_dist = 32767
        candidate_rects = None
        for r in rects:
            dist = self.compare(r)
            if dist < min_dist:
                min_dist = dist
                candidate_rect = r
        if min_dist < self.feature_dist_threshold:
            history_size = len(self.rect_history)
            self.rect_history.append(candidate_rect)
            feature = []
            for i in range(4):
                for j in range(2):
                    feature.append(candidate_rect.corners()[i][j])
            if history_size <  self.window_size:
                for i in range(8):
                    self.feature_vector[i] = (self.feature_vector[i]*history_size +
                        feature[i])/(history_size + 1)
                self.untracked_frames = 0
                print("replaced! {}".format(min_dist))
            else:
                oldest_rect = self.rect_history[0]
                oldest_feature = []
                for i in range(4):
                    for j in range(2):
                        oldest_feature.append(oldest_rect.corners()[i][j])
                for i in range(8):
                    self.feature_vector[i] = (self.feature_vector[i]*self.window_size +
                        feature[i] - oldest_feature[i])/self.window_size
                self.rect_history.pop(0)
            return True
        else:
            self.untracked_frames += 1
            return False
slow_led = False
time_start = time.time_ns()
cx = 0
cy = 0
size_goal_blob = 0
def difference_goal_blob():
    global time_start
    global cx
    global cy
    global size_goal_blob
    clock.tick()
    omv.disable_fb(False)
    found_blobs = False
    elapsed = 24000 - (int((time.time_ns()-time_start)/1000))
    if elapsed > 0:
        time.sleep_us(elapsed)
#    extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)
#    extra_fb.replace(sensor.snapshot())
    image0 = sensor.snapshot().copy()
    time_start = time.time_ns()
    led_pin.value(0)
    elapsed = 24000 - (int((time.time_ns()-time_start)/1000))
    if elapsed > 0:
        time.sleep_us(elapsed)
    img = sensor.snapshot()
    time_start = time.time_ns()
    img.sub(image0, reverse = True)
#    sensor.dealloc_extra_fb()
    led_pin.value(1)
    img.lens_corr(1.65)
    img.negate()
    sensor.flush()
    omv.disable_fb(True)

    green_blobs = img.find_blobs([green_threshold],
                   merge=True,
                   area_threshold=0,
                   pixels_threshold=0,
                   margin = 15)
    rects = []
    orange_blobs = img.find_blobs([orange_threshold],
                   merge=True,
                   area_threshold=0,
                   pixels_threshold=0,
                   margin = 15)
    rects = []
    if orange_blobs:
        for orange_blob in orange_blobs:
            img.draw_rectangle(orange_blob.rect(), color = (255,0,0))
        the_blob = find_max(orange_blobs)
        st = "FPS: {}".format(str(round(clock.fps(),2)))
        img.draw_string(0, 0, st, color = (255,0,0))
        new_cx = the_blob.cx()
        new_cy = the_blob.cy()
        new_size_goal_blob = max(the_blob.w(), the_blob.h())
        vx = new_cx - cx
        cx = new_cx
        vy = new_cy - cy
        cy = new_cy
        vsize = new_size_goal_blob - size_goal_blob
        size_goal_blob = new_size_goal_blob
        return struct.pack("<BBHh",
            True,
            True,
            cx,
            vx
        )
    if green_blobs:
        for green_blob in green_blobs:
            img.draw_rectangle(green_blob.rect(), color = (0,255,0))
        the_blob = find_max(green_blobs)
        st = "FPS: {}".format(str(round(clock.fps(),2)))
        img.draw_string(0, 0, st, color = (255,0,0))
        new_cx = the_blob.cx()
        new_cy = the_blob.cy()
        new_size_goal_blob = max(the_blob.w(), the_blob.h())
        vx = new_cx - cx
        cx = new_cx
        vy = new_cy - cy
        cy = new_cy
        vsize = new_size_goal_blob - size_goal_blob
        size_goal_blob = new_size_goal_blob
        return struct.pack("<BBHh",
            True,
            False,
            cx,
            vx
        )
    return struct.pack("<BBHh", False, False, 0, 0)
def find_max(blobs):
    max_blob = None
    max_area = 0
    for blob in blobs:
        if blob.area() > max_area:
            max_blob = blob
            max_area = blob.pixels()
    return max_blob
def blob_detection(clock, show = True):
    global tracked_blob
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([purple_threshold],
                           merge=True,
                           area_threshold=25,
                           pixels_threshold=15)
    if tracked_blob == None:
        max_blob = find_max(blobs)
        if max_blob:
            red_led.on()
            tracked_blob = TrackedBlob(max_blob, norm_level=2,
                                       feature_dist_threshold=20,
                                       window_size = 5)
            x, y, z = verbose_tracked_blob(img, tracked_blob, show)
            return x, y, z, True
        else:
            red_led.off()
            return -1, -1, -1, False
    else:
        red_led.on()
        tracked_blob.update(blobs)
        if tracked_blob.untracked_frames >= 30:
            tracked_blob = None
            red_led.off()
            print("boom!")
            return -1, -1, -1, False
        else:
            x, y, z = verbose_tracked_blob(img, tracked_blob, show)
            return x, y, z, True
def verbose_tracked_blob(img, tracked_blob, show):
    if framesize == sensor.HQVGA:
        x_size = 240
        y_size = 160
    elif framesize == sensor.QQVGA:
        x_size = 160
        y_size = 120
    else:
        assert(False)
    linear_regression_feature_vector = [0 ,0, 0, 0]
    num_blob_history = len(tracked_blob.blob_history)
    for i in range(num_blob_history):
        linear_regression_feature_vector[0] += tracked_blob.blob_history[i].cx()
        linear_regression_feature_vector[1] += tracked_blob.blob_history[i].cy()
        linear_regression_feature_vector[2] += tracked_blob.blob_history[i].w()
        linear_regression_feature_vector[3] += tracked_blob.blob_history[i].h()
    for i in range(4):
        linear_regression_feature_vector[i] /= num_blob_history
    feature_vec = [linear_regression_feature_vector[0]/x_size,
                   linear_regression_feature_vector[1]/y_size,
                   math.sqrt(x_size*y_size/(linear_regression_feature_vector[2]*
                             linear_regression_feature_vector[3]))]
    dist = 0.27485909*feature_vec[2] + 0.9128014726961156
    theta = -0.98059103*feature_vec[0] + 0.5388727340530889
    phi = -0.57751757*feature_vec[1] + 0.24968235246037554
    z = dist*math.sin(phi)
    xy = dist*math.cos(phi)
    x = xy*math.cos(theta)
    y = xy*math.sin(theta)
    if show:
        x0, y0, w, h = [math.floor(tracked_blob.feature_vector[i]) for i in range(4)]
        img.draw_rectangle(x0, y0, w, h)
        st = "FPS: {}".format(str(round(clock.fps(),2)))
        img.draw_string(0, 0, st, color = (255,0,0))
    return x, y, z
def init_sensor(pixformat=sensor.RGB565, framesize=sensor.HQVGA, windowsize=None,
                gain=18, autoexposure=False, exposure=10000, autowhitebal=False,
                white_balance=(0, 0, 0),
                contrast=0, saturation=0):
    sensor.reset()
    sensor.set_pixformat(pixformat)
    sensor.set_framesize(framesize)
    if windowsize:
        sensor.set_windowing(windowsize)
    sensor.skip_frames(time = 1000)
    # sensor.set_auto_gain(False, gain_db=gain)
    sensor.set_auto_whitebal(autowhitebal, rgb_gain_db=white_balance)
    sensor.set_auto_whitebal(True)
    sensor.set_auto_exposure(autoexposure, exposure_us=exposure)
    sensor.set_contrast(contrast)
    sensor.set_saturation(saturation)
    sensor.skip_frames(time = 1000)
    sensor.__write_reg(0x0E, 0b00000000)
    sensor.__write_reg(0x3E, 0b00000000)
    sensor.skip_frames(time = 1000)
    clock = time.clock()
    led_pin = Pin("PC4", Pin.OUT)
    return led_pin, clock
def convert_data_goal(tracked_rect, data):
    data[0] = 1
    if tracked_rect != None:
        data[5] = 0
        blx,bly,brx,bry,ulx,uly, urx,ury = tracked_rect.feature_vector
        mx = (ulx + urx + blx + brx)/4
        my = (uly + ury + bly + bry)/4
        u = ((urx-ulx)**2 + (ury-uly)**2)**.5
        l = ((ulx-blx)**2 + (uly-bly)**2)**.5
        b = ((brx-blx)**2 + (bry-bly)**2)**.5
        r = ((urx-brx)**2 + (ury-bry)**2)**.5
        x = int((mx - sensor.width()/2) * 127 / sensor.width())
        y = int((my - sensor.height()/2) * 127 / sensor.height())
        w = int(clamp(1/max(u,l,b,r)*1000, 0, 40)/40 * 127)
        s = int(clamp((r-l)/10,-1,1)*127)
        data[1] = x
        data[2] = y
        data[3] = int(data[3] * .9 + w * .1)
        data[4] = int(data[4] * .9 + s * .1)
        print(data[1:5])
    else:
        if data[5] < 127:
            data[5] += 1
    return data
def convert_data_blob(x,y,z,seen, data):
    data[0] = 0
    if seen:
        data[5] = 0
        data[1] = int((clamp(x, -5,5)/5)*127)
        data[2] = int((clamp(x, -5,5)/5)*127)
        data[3] = int((clamp(x, -5,5)/5)*127)
        data[4] = 0
    else:
        if data[5] < 127:
            data[5] += 1
    return data
def convert_data_light(w,m, data):
    data[0] = 1
    data[5] = 0
    data[1] = int((clamp(w, -1,1)/1)*127)
    data[2] = 0
    data[3] = int((clamp(m, 0,1)/1)*127)
    data[4] = 0
    return data
def send_through_uart(data, uart_port):
    msg = bytearray(8)
    msg[0] = 0x69
    msg[1] = 0x69
    msg[2] = data[0]
    msg[3] = data[1]
    msg[4] = data[2]
    msg[5] = data[3]
    msg[6] = data[4]
    msg[7] = data[5]
    print(data)
    uart_port.write(msg)
def setup_network(ssid, key):
    network_if = network.WLAN(network.STA_IF)
    network_if.active(True)
    network_if.connect(ssid, key)
    return network_if
class MyCustomException(Exception):
    pass
def throw_end(data):
    raise MyCustomException("-1")
def throw_blob(data):
    raise MyCustomException("0")
def throw_goal(data):
    raise MyCustomException("1")
def throw_auto(data):
    raise MyCustomException("2")
def loop_interrupt(data = None):
    raise MyCustomException("3")
def setInterface(network_if):
    interface = rpc.rpc_network_slave(network_if)
    interface.register_callback(throw_end)
    interface.register_callback(throw_blob)
    interface.register_callback(throw_goal)
    interface.register_callback(throw_auto)
    interface.setup_loop_callback(loop_interrupt)
    return interface
def startGoalBlob(network_if):
    interface = rpc.rpc_network_slave(network_if)
    interface.register_callback(difference_goal_blob)
    print("looping")
    interface.loop(recv_timeout=1000, send_timeout=1000)
def getFlag(interface, network_if, base):
    if network_if.isconnected():
        flag = -1
        try:
            interface.loop(recv_timeout=250, send_timeout=250)
        except MyCustomException as e:
            flag = int(f"{e}")
            if flag == 3:
                flag = base
            print(f"caught: {e}")
        return flag
    else:
        return base
def light_following():
    n_cols, n_rows = int(sensor.width()/2), sensor.height()
    img = sensor.snapshot()
    l = 0
    r = 0
    n_pixels = 0
    for j in range(n_rows):
        for i in range(n_cols):
            l += img.get_pixel(i, j)
            r += img.get_pixel(sensor.width() - n_cols + i , j)
            n_pixels += 1
    l /= 255 * n_pixels
    r /= 255 * n_pixels
    w = r - l
    m = (r + l) / 2
    w = 1 if w>0 else -1
    msg = "w=" + str(w) + " m=" + str(m)
    return w, m
if __name__ == "__main__":
    networking = False
    night = False
    show = True
    lightfollow = False
    flag = 1
    network_if = None
    interface = None
    framesize = sensor.QQVGA
    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    blue_led = pyb.LED(3)
    if lightfollow:
        led_pin, clock = init_sensor(pixformat=sensor.GRAYSCALE,
            framesize=framesize, windowsize=None,
            gain=-50, autoexposure=False,
            exposure=100, autowhitebal=False,
            contrast=-3, saturation=0)
    elif flag == 1:
        led_pin, clock = init_sensor(pixformat=sensor.RGB565,
            framesize=framesize, windowsize=None,
            gain=6, autoexposure=False,
            exposure=5000, autowhitebal=False,
            white_balance=(-6.02073, -5.49487, -1.804),
            contrast=-3, saturation=0)
    elif flag == 0:
        led_pin, clock = init_sensor(pixformat=sensor.RGB565,
            framesize=framesize, windowsize=None,
            gain=12, autoexposure=False,
            exposure=10000, autowhitebal=False,
            white_balance=(-5.02073, -5.49487, -0.804),
            contrast=-3, saturation=3)
    quick = True
    extra_fb = None
    if not quick:
        extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)
        extra_fb.replace(sensor.snapshot())
    time_start = time.time_ns()
    tracked_blob = None
    tracked_rect = None
    state = 0
    print("getting started")
    if networking:
        SSID='AIRLab-BigLab'
        KEY='Airlabrocks2022'
        network_if = setup_network(SSID,KEY)
        while not network_if.isconnected():
            print(".")
            network_if = setup_network(SSID,KEY)
    while(True):
        difference_goal_blob()
    # startGoalBlob(network_if)
#    while(True):
#        if networking:
#            if (time.time_ns() -flag_last)/1000000000 > 10:
#                test = time.time_ns()
#                flag = getFlag(interface, network_if, flag)
#                flag_last = time.time_ns()
#                print("connection time: ", (flag_last - test)/1000000000)
#        if lightfollow:
#            w, m = light_following()
#            data = convert_data_light(w,m,data)
#            send_through_uart(data, uart)
#        elif flag == -1:
#            break
#        elif flag == 0: #blob detection
#            led_pin.value(0)
#            x,y,z,seen = blob_detection(clock, show = show) #this is where it is supposed to go
#            data = convert_data_blob(x,y,z,seen,data)
#            send_through_uart(data, uart)
#        elif flag == 1: #goal detection
#            time_start, tracked_rect = difference_goal_rect(clock, time_start, led_pin,extra_fb, tracked_rect,night , show, quick)
#            data = convert_data_goal(tracked_rect, data)
#            send_through_uart(data, uart)
#        elif flag == 2: #fully auto
#            if balls_caught < 2:
#                x,y,z,seen = blob_detection(clock, show = True)
#            else:
#                time_start, tracked_rect = difference_goal_rect(clock, time_start, led_pin,extra_fb, tracked_rect,night , show, quick)
#                data = convert_data_goal(tracked_rect, data)
#            if scoring:
#                state = 4
#            elif balls_caught < 2:
#                if seen:
#                    state = 1
#                else:
#                    state = 0
#            else:
#                if seen:
#                    state = 3
#                else:
#                    state = 2
#        #print(clock.fps())'''
