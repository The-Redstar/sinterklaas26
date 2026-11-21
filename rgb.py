
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
    0: Color(  0,  0,  0),
    1: Color(255,  0,  0),
    2: Color(  0,255,  0),
    3: Color(255,255,  0),
    4: Color(  0,  0,255),
    5: Color(255,  0,255),
    6: Color(  0,255,255),
    7: Color(255,255,255),
}
COLORS["red"]=COLORS[1]
COLORS["green"]=COLORS[2]
COLORS["blue"]=COLORS[4]

BLINKING_COLORS=COLORS.copy()
BLINKING_COLORS[0]=Color(50,50,50)

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
        sleep(50)
