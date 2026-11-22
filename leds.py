
import RPi.GPIO as GPIO

from rgb import BLINK, OFF

ON = 0

GPIO.setmode(GPIO.BCM)
PIN_I1=21
PIN_I2=20
PIN_I3=16
PIN_B5_I=12

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
