import time

import adafruit_pcf8523
import board
import busio
import neopixel

INTERVAL = 5 * 60

NOW = time.struct_time((2022, 10, 6, 13, 55, 0, 0, -1, -1))
SET_TIME = False

light_data = [
    (0.0, (0.0, (0, 0, 0, 0))),
    (7.0, (0.1, (244, 254, 169, 0))),
    (8.0, (0.2, (243, 254, 174, 0))),
    (13.0, (1.0, (234, 254, 202, 0))),
    (18.0, (0.2, (243, 254, 174, 0))),
    (19.0, (0.1, (244, 254, 169, 0))),
    (24.0, (0.0, (0, 0, 0, 0))),
]

pixels = neopixel.NeoPixel(
    board.D6, 24, brightness=1.0, auto_write=False, pixel_order=neopixel.RGBW
)

i2c = busio.I2C(board.SCL1, board.SDA1)
rtc = adafruit_pcf8523.PCF8523(i2c)


if SET_TIME:
    rtc.datetime = NOW


def lerp(begin, end, t):
    return begin + t * (end - begin)


def time2float(h, m):
    return float(h) + float(m) / 60.0


def get_light_lerp(daytime):
    pt, (pb, pc) = (0, (0, (0, 0, 0, 0)))

    for t, (b, c) in light_data:
        if t == daytime:
            print("{}: {} @ {}".format(t, c, b))
            return (b, c)
        if t < daytime:
            pt, pb, pc = t, b, c
            continue
        lt = (daytime - pt) / (t - pt)
        lb = lerp(pb, b, lt)
        lc = tuple(int(lerp(pc[i], v, lt)) for i, v in enumerate(c))
        print("{} -> {} ({}): {} @ {}".format(pt, t, lt, lc, lb))
        return (lb, lc)


def set_light(brightness, color):
    pixels.fill(tuple(int(v * brightness) for v in color))
    pixels.show()


i = 0
while True:
    dt = rtc.datetime
    t = time2float(dt.tm_hour, dt.tm_min)
    print(t)
    if i == 0:
        set_light(*get_light_lerp(t))
    i += 1
    if i > INTERVAL:
        i = 0
        continue
    time.sleep(1)
