
from pins import *
from buttons import Buttons
from rgb import OFF

import types

class Inputs:
    def __init__(self):
        self.buttons = Buttons(
            (PIN_B1,1,0),
            (PIN_B2,2,0),
            (PIN_B3,4,0),
            PIN_B4,
            PIN_B5,
            PIN_K,
            PIN_LO,
            (PIN_HI,False,True)
        )

    def get(self):
        b1,b2,b3,b4,b5,k,lo,hi=self.buttons.get()
        return types.SimpleNamespace(
            b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,k=k,lo=lo,hi=hi,
            b123=b1+b2+b3,
            b123_c=(1 if b1 else OFF, 2 if b2 else OFF, 4 if b3 else OFF),
            diff=int(hi)-int(lo),
        )

