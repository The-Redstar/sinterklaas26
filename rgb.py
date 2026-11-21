
from rpi_ws281x import PixelStrip, Color
import time

# LED configuration
LED_COUNT = 3
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100  # 0-255
LED_INVERT = False
LED_CHANNEL = 0

COLORS = {
    0: Color( 10, 10, 10),
    1: Color(255,  0,  0),
    2: Color(  0,255,  0),
    3: Color(255,255,  0),
    4: Color(  0,  0,255),
    5: Color(255,  0,255),
    6: Color(  0,255,255),
    7: Color(255,255,255),
    8: Color(0,0,0),
}

BLACK=0
RED=1
GREEN=2
BLUE=4
YELLOW=3
MAGENTA=5
CYAN=6
WHITE=7
OFF=8

BLINKING_COLORS=COLORS.copy()
# BLINKING_COLORS[BLACK]=Color(10,10,10)

SOLID="solid"
BLINK="blink"

class RGB:
    def __init__(self):
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL
        )
        self.strip.begin()
        self.state = [0,0,0]

    def update(self,t=0):
        for i in range(3):
            try:
                mode,color = self.state[i]
            except:
                mode = SOLID
                color = self.state[i]
            if mode==SOLID:
                self.strip.setPixelColor(i,COLORS[color])
            else:
                if int(t*1000)%500 < 250:
                    self.strip.setPixelColor(i,BLINKING_COLORS[color])
                else:
                    self.strip.setPixelColor(i,COLORS[0])
        self.strip.show()

    def set(self,l,m,r):
        self.state = [l,m,r]
        





if __name__=="__main__":
    from time import time,sleep

    rgb = RGB()
    rgb.set("red",(BLINK,6),(BLINK,0))
    
    while True:
        rgb.update(time())
        sleep(0.050)
