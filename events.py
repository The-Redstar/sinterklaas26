

import types

events = types.SimpleNamespace()

events.PRESSED="pressed"
events.RELEASED="released"
events.UPDATE="update"

PRESSED=lambda key:(events.PRESSED,key)
RELEASED=lambda key:(events.RELEASED,key)

class EventGenerator:
    def __init__(self,init):
        self.prev=init
    def gen(self,state):
        out=[]
        if state.b1!=self.prev.b1:
            if state.b1:
                out.append(PRESSED(1))
            else:
                out.append(RELEASED(1))

        if state.b2!=self.prev.b2:
            if state.b2:
                out.append(PRESSED(2))
            else:
                out.append(RELEASED(2))

        if state.b3!=self.prev.b3:
            if state.b3:
                out.append(PRESSED(4))
            else:
                out.append(RELEASED(4))

        if state.b4!=self.prev.b4:
            if state.b4:
                out.append(PRESSED("ok"))
            else:
                out.append(RELEASED("ok"))

        if state.b5!=self.prev.b5:
            if state.b5:
                out.append(PRESSED("launch"))
            else:
                out.append(RELEASED("launch"))

        if state.k!=self.prev.k:
            if state.k:
                out.append(PRESSED("key"))
            else:
                out.append(RELEASED("key"))

        out.append(events.UPDATE)

        self.prev=state
        return out
