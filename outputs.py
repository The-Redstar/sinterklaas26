
import rgb
import servo
import leds
from pins import *

import time


class Outputs:
    def __init__(self):
        self.rgb = rgb.RGB()
        self.dial = servo.Dial()
        self.leds = leds.Leds(PIN_I1,PIN_I2,PIN_I3)
        self.button = leds.Leds(PIN_B5_I)

    def update(self):
        t = time.time()
        b = int(t*1000)%500<250

        # servo updates immediately
        self.rgb.update(b)
        self.leds.update(b)
        self.button.update(b)

if __name__=="__main__":
    from rgb import *
    from leds import *

    outputs = Outputs()
    outputs.rgb.set(RED,BLUE+BLINK,GREEN)
    outputs.dial.set(4)
    outputs.leds.set(BLINK,OFF,ON)
    outputs.button.set(ON)

    while True:
        outputs.update()
        time.sleep(0.05)
