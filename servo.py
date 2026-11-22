try:
    from gpiozero import AngularServo
    from gpiozero.pins.pigpio import PiGPIOFactory
except:
    from dummy import AngularServo, PiGPIOFactory

from pins import *

class Dial:
    def __init__(self):
        self.factory = PiGPIOFactory()

        self.servo = AngularServo(
            PIN_SERVO,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0024,
            pin_factory=self.factory
        )

    def set(self,angle):
        self.servo.angle=150-angle*(120/8)
    
    def exit(self):
        self.servo.detach()


if __name__=="__main__":
    from time import sleep

    dial = Dial()

    try:
        while True:
            dial.set(0)
            sleep(2)

            dial.set(90)
            sleep(1)

            dial.set(180)
            sleep(1)
    except KeyboardInterrupt:
        dial.exit()
