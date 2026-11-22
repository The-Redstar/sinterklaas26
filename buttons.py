
try:
    import RPi.GPIO as GPIO
except:
    from dummy import GPIO

from pins import *

class Buttons:
    def __init__(self,*buttons):
        self.buttons = []
        for b in buttons:
            try:
                (p,vl,vh) = b
            except:
                p=b
                vl=True
                vh=False
            GPIO.setup(p,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            self.buttons.append((p,vl,vh))

    def get(self):
        res = []
        for (p,vl,vh) in self.buttons:
            if GPIO.input(p)==GPIO.LOW:
                res.append(vl)
            else:
                res.append(vh)
        return tuple(res)
        

if __name__=="__main__":
    from outputs import *
    from rgb import *
    import time

    outputs = Outputs()
    buttons = Buttons(
        (PIN_B1,RED,OFF),
        (PIN_B2,GREEN,OFF),
        (PIN_B3,BLUE,OFF),
        PIN_B4,
        PIN_B5,
        PIN_K,
        PIN_LO,
        (PIN_HI,False,True)
    )

    while True:
        b1,b2,b3, b4,b5, k, lo,hi = buttons.get()

        outputs.rgb.set(b1,b2,b3)
        outputs.button.set(b5)
        outputs.leds.set(b4,k,lo and hi)

        if lo and hi:
            outputs.dial.set(90)
        elif lo:
            outputs.dial.set(120)
        elif hi:
            outputs.dial.set(60)
        else:
            outputs.dial.set(90)
        
        outputs.update()
        time.sleep(0.05)

