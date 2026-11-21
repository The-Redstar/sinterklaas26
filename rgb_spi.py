import spidev

LED_COUNT = 3

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 2400000
spi.mode = 0

pixels = [(0, 0, 0)] * LED_COUNT


def encode_byte(value):
    """Encode 8 WS2812 bits into 24 SPI bits."""
    encoded = 0

    for bit in range(7, -1, -1):
        encoded = (encoded << 3) | (0b110 if value & (1 << bit) else 0b100)

    return [
        (encoded >> 16) & 255,
        (encoded >> 8) & 255,
        encoded & 255
    ]


def show():
    data = []

    for r, g, b in pixels:
        # WS2812 expects GRB order
        for value in (g, r, b):
            data.extend(encode_byte(value))

    # Reset/latch period: 200 microseconds
    data.extend([0] * 60)

    spi.xfer2(data)


def set_pixel(index, r, g, b):
    pixels[index] = (r, g, b)
    show()


def set_all(r, g, b):
    for i in range(LED_COUNT):
        pixels[i] = (r, g, b)
    show()


def clear():
    set_all(0, 0, 0)


def close():
    clear()
    spi.close()

if __name__=="__main__":
    import time

    set_pixel(0, 255, 0, 0)
    set_pixel(1, 0, 255, 0)
    set_pixel(2, 0, 0, 255)

    time.sleep(15)

    rgb.set_all(255, 255, 255)
    time.sleep(5)

    rgb.close()
