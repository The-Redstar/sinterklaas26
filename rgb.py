
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

# Initialize LED strip
strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL
)

strip.begin()


if __name__=="__main__":
    def set_all(r, g, b):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(r, g, b))
        strip.show()

    try:
        while True:
            set_all(255, 0, 0)  # Red
            time.sleep(1)

            set_all(0, 255, 0)  # Green
            time.sleep(1)

            set_all(0, 0, 255)  # Blue
            time.sleep(1)

    except KeyboardInterrupt:
        set_all(0, 0, 0)
