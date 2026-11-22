from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()

servo = AngularServo(
    13,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0024,
    pin_factory=factory
)

try:
    while True:
        servo.angle = 0
        sleep(1)

        servo.angle = 90
        sleep(1)

        servo.angle = 180
        sleep(1)

except KeyboardInterrupt:
    servo.detach()
