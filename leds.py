
try:
    import RPi.GPIO as GPIO
except:
    from dummy import GPIO

from rgb import BLINK, OFF
from pins import *

ON = 0

GPIO.setmode(GPIO.BCM)


class Leds:
    def __init__(self,*pins):
        self.pins = pins
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
        self.states = [OFF for _ in pins]

    def set(self,*states):
        self.states=states

    def update(self,blink_on=True):
        for p,s in zip(self.pins,self.states):
            if s is True:
                GPIO.output(p,GPIO.HIGH)
            elif s is False:
                GPIO.output(p,GPIO.LOW)
            elif s==ON or (s==BLINK and blink_on):
                GPIO.output(p,GPIO.HIGH)
            else:
                GPIO.output(p,GPIO.LOW)
            
if __name__=="__main__":
    import time

    leds = Leds(PIN_I1,PIN_I2,PIN_I3)
    leds.set(ON,BLINK,OFF)

    b=True
    while True:
        leds.update(b)
        b=not b
        time.sleep(0.250)
