from gpiozero import AngularServo
from time import sleep

servo = AngularServo(
    13,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0024
)

try:
    while True:
        servo.angle = 0
        sleep(2)

        servo.angle = 90
        sleep(1)

        servo.angle = 180
        sleep(1)

except KeyboardInterrupt:
    servo.detach()
