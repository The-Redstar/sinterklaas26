
from inputs import Inputs
from events import *

from outputs import Outputs
from rgb import *
from leds import *
from printer import Printer
from pages import *
from persistent import *

import steam
import memory

import types
import time

try:
    import RPi.GPIO
except:
    DUMMY=True
    from dummy import dummy
else:
    DUMMY=False

states=types.SimpleNamespace()
states.START="start"
states.INDEXING="index"
states.PAGE="page"
states.FAILED="failed"
states.SUCCEEDED="succeeded"
states.FINISHED="finished"
states.STEAM="steam"
states.MEMORY="memory"
states.KEY="key"

pages=types.SimpleNamespace()
pages.STEAM=(2,6,6)
pages.MEMORY=(2,3,7)
pages.KEY=(2,4,1)
pages.FINAL=(5,1,2)

MEMORY_TIME_LIMIT = 10
MEMORY_TIME_BONUS = 3

class Machine:
    def __init__(self):
        self.inputs=Inputs()
        self.outputs=Outputs()
        self.printer=Printer()
        self.persistent=Persistent()

        self.inp=self.inputs.get()
        self.event_generator=EventGenerator(self.inp)

        self.state=None
        self.meta=None
        self.handler=lambda e:None
        self.next_state = None

        self(states.START)

    def __call__(self,state):
        print("CALL",state)
        self.next_state = state

    def set_state(self,state):
        prev_state = self.state
        self.state=state
        self.next_state = None

        print("STATE SWITCH:",state)

        match state:
            case states.START:
                if self.persistent.has(FINAL_COMPLETED):
                    self.persistent.clear()
                self.output()
                self.print("000")
                self(states.INDEXING)
            
            # in between pages
            case states.INDEXING:
                self.meta = []
                self.handler = self.handle_index
                self.output()

            # pages
            case (states.PAGE,pages.FINAL):
                ready = (
                    self.persistent.has(STEAM_COMPLETED) and self.persistent.has(MEMORY_COMPLETED) and self.persistent.has(KEY_COMPLETED)
                    and not self.persistent.has(FINAL_COMPLETED))
                self.meta = ready
                self.handler = self.handle_final
                if self.persistent.has(FINAL_COMPLETED):
                    self.output()
                    self.print("512C")
                elif ready:
                    self.output(button=True)
                    self.print("512B")
                else:
                    self.output()
                    self.print("512A")
            case (states.PAGE,pages.STEAM):
                self.meta = types.SimpleNamespace(all_pressed=False)
                self.handler = self.handle_test(states.STEAM)
                self.output(leds=(ON if self.persistent.has(STEAM_COMPLETED) else BLINK,None,None))
                match prev_state:
                    case (states.SUCCEEDED | states.FAILED,_):
                        pass
                    case _:
                        self.print(pages.STEAM)
            case (states.PAGE,pages.MEMORY):
                self.meta = types.SimpleNamespace(all_pressed=False)
                self.handler = self.handle_test(states.MEMORY)
                self.output(leds=(None,ON if self.persistent.has(MEMORY_COMPLETED) else BLINK,None))
                match prev_state:
                    case (states.SUCCEEDED | states.FAILED,_):
                        pass
                    case _:
                        self.print(pages.MEMORY)
            case (states.PAGE,pages.KEY):
                self.meta = types.SimpleNamespace(all_pressed=False)
                self.handler = self.handle_test(states.KEY)
                self.output(leds=(None,None,ON if self.persistent.has(KEY_COMPLETED) else BLINK))
                match prev_state:
                    case (states.SUCCEEDED | states.FAILED,_):
                        pass
                    case _:
                        self.print(pages.KEY)
            case (states.PAGE,page):
                self.meta = None
                self.handler = self.handle_page
                self.output()
                self.print(page)
            
            # actual tests running
            case states.STEAM:
                self.meta = types.SimpleNamespace(
                    start=time.time(),
                    recorded=[],
                    pressure=0,
                    samples=steam.gen(50),
                    index=0,
                    failed=False,
                    completed=False,
                )
                self.handler = self.handle_steam
                self.output(leds=(BLINK,None,None),rgb=(BLACK,BLACK,BLACK))
            case states.MEMORY:
                sig = memory.generate()
                ans = memory.answer(sig)
                print("SIG",sig)
                print("ANS",ans)
                self.meta = types.SimpleNamespace(
                    signal=sig,
                    answer=ans,
                    state=("display",1), #display 1 -> input 1 -> display 2 -> input 2...
                    start=time.time(),
                    inputs=[],
                )

                self.handler = self.handle_memory
                self.output(leds=(None,BLINK,None),rgb=(BLACK,BLACK,BLACK))
            case states.KEY:
                self.meta = types.SimpleNamespace(start=time.time())
                self.handler = self.handle_key
                self.output(leds=(None,None,BLINK),rgb=(BLACK,BLACK,BLACK))

            case (states.SUCCEEDED,page):
                self.meta = types.SimpleNamespace(start=time.time())
                self.handler = self.handle_completed
                self.outputs.rgb.set(GREEN,GREEN,GREEN)
                self.print(page+("A",))
            case (states.FAILED,page):
                self.meta = types.SimpleNamespace(start=time.time())
                self.handler = self.handle_completed
                self.outputs.rgb.set(RED,RED,RED)
                self.print(page+("B",))
            
            case states.FINISHED:
                self.persistent.set(FINAL_COMPLETED)
                self.meta = None
                self.handler = handle_page
                self.output()
                self.print("FINISHED")


    def handle_index(self,e):
        match e:
            case (events.PRESSED,"ok"):
                self.meta.append(self.inp.b123)
                if len(self.meta)==3:
                    self((states.PAGE,tuple(self.meta)))
            case events.UPDATE:
                colors = self.meta + [BLINK + self.inp.b123] + [OFF,OFF]
                colors=colors[:3]
                #print(colors)
                self.outputs.rgb.set(*colors)

    def handle_page(self,e):
        match e:
            case (events.PRESSED,"ok"):
                self(states.INDEXING)

    def handle_test(self,test_state):
        def handler(e,self=self,test_state=test_state):
            self.handle_test_(e,test_state)
        return handler
    def handle_test_(self,e,test_state):
        match e:
            case (events.PRESSED,int()): #buttons must first all be pressed
                if self.inp.b123==7:
                    self.meta.all_pressed=True
                    self.outputs.rgb.set(WHITE,WHITE,WHITE)
            case (events.RELEASED,int()): # and then all released
                if self.inp.b123==0 and self.meta.all_pressed:
                    self(test_state)
            case _:
                self.handle_page(e)



    def handle_steam(self,e):
        match e:
            case events.UPDATE:
                r = self.meta.recorded + [None,None,None]
                c = {None: BLACK, 0:GREEN, 1:YELLOW, 5:RED}
                self.outputs.rgb.set(
                    c[r[0]],
                    c[r[1]],
                    c[r[2]],
                )

                if self.meta.failed or self.meta.completed:
                    if time.time()-self.meta.stop>=1:
                        if self.meta.completed:
                            self.persistent.set(STEAM_COMPLETED)
                            self((states.SUCCEEDED,pages.STEAM))
                        if self.meta.failed:
                            print("WRONG PRESSURE")
                            self((states.FAILED,pages.STEAM))
                    return

                duration = time.time() - self.meta.start
                if (duration>=(len(self.meta.recorded)+1)*12):
                    target = [7,2,5,0][len(self.meta.recorded)]
                    diff = abs(target-self.meta.pressure)
                    if diff<0.5:
                        self.meta.recorded.append(0)
                    elif diff<1:
                        self.meta.recorded.append(1)
                    else:
                        self.meta.recorded.append(5)
                    
                    if sum(self.meta.recorded)>1:
                        self.meta.stop=time.time()
                        self.meta.failed=True
                        return

                    if len(self.meta.recorded)==3: # passed
                        self.meta.stop=time.time()
                        self.meta.completed=True
                        return
                
                # update pressure level based on inputs
                self.meta.pressure += (self.inp.diff+max(-0.9,min(0.9,self.meta.samples[self.meta.index]*1.2)))*1.0*0.050
                self.meta.index+=1

                self.meta.pressure = max(0,self.meta.pressure)
                if self.meta.pressure > 9:
                    print("EXPLODE")
                    self((states.FAILED,pages.STEAM))
                
                self.outputs.dial.set(self.meta.pressure)

    def handle_memory(self,e):
        global MEMORY_TIME_LIMIT
        if self.next_state:
            return
        match self.meta.state:
            case ("display",l):
                match e:
                    case events.UPDATE:
                        self.outputs.dial.set(8)
                        dt = int(time.time()-self.meta.start)-3

                        if dt<0: # first couple seconds, do nothing
                            self.outputs.rgb.set(*self.inp.b123_c)
                            return

                        if dt%2==1:
                            self.outputs.rgb.set(OFF,OFF,OFF)
                            if dt//2==l-1:
                                self.meta.state=("input",l)
                                self.meta.start=time.time()
                                self.meta.inputs=[]
                        else:
                            self.outputs.rgb.set_simple(*self.meta.signal[dt//2])

            case ("input",l):
                match e:
                    case (events.PRESSED,int(k)):
                        self.meta.inputs.append(k)

                        if self.meta.inputs != self.meta.answer[:len(self.meta.inputs)]:
                            print("WRONG KEY")
                            self((states.FAILED,pages.MEMORY))
                            return
                        
                        if len(self.meta.inputs)==5: # done
                            print("ACCEPTED")
                            self.persistent.set(MEMORY_COMPLETED)
                            self((states.SUCCEEDED,pages.MEMORY))
                            return
                        
                        if len(self.meta.inputs)==l:
                            self.meta.state=("display",l+1)
                            self.meta.start=time.time()

                    case events.UPDATE:
                        dt = time.time()-self.meta.start

                        time_remaining = MEMORY_TIME_LIMIT + len(self.meta.inputs)*MEMORY_TIME_BONUS - dt

                        if time_remaining <= 0:
                            print("TIMEOUT")
                            MEMORY_TIME_LIMIT+=2
                            self((states.FAILED,pages.MEMORY))

                        self.outputs.dial.set(min(8,time_remaining))
                        
                        self.outputs.rgb.set(*self.inp.b123_c)

    def handle_key(self,e):
        match e:
            case (events.PRESSED,"key"):
                self.persistent.set(KEY_COMPLETED)
                self((states.SUCCEEDED,pages.KEY))
            case events.UPDATE:
                if self.next_state: #break race condition
                    return
                dt = time.time()-self.meta.start
                self.outputs.dial.set(min(8,10-dt))
                if dt>10:
                    print("TIMEOUT")
                    self((states.FAILED,pages.KEY))
    



    def handle_completed(self,e):
        match e:
            case events.UPDATE:
                if time.time()-self.meta.start>2:
                    self((states.PAGE,self.state[1]))

    def handle_final(self,e):
        match e:
            case (events.PRESSED,"launch"):
                if self.meta:
                    self(states.FINISHED)
            case _:
                self.handle_page(e)











    def output(self,rgb=None,leds=(None,None,None),dial=0,button=False):
        if rgb is None:
            match self.state:
                case (states.PAGE,(a,b,c)):
                    rgb=(a,b,c)
                case _:
                    rgb=(OFF,OFF,OFF)
        
        leds=list(leds)
        for i in range(3):
            if leds[i] is None:
                leds[i] = self.persistent.has([STEAM_COMPLETED,MEMORY_COMPLETED,KEY_COMPLETED][i])

        self.outputs.rgb.set(*rgb)
        self.outputs.leds.set(*leds)
        self.outputs.button.set(button)
        self.outputs.dial.set(dial)

    def update(self):
        self.inp = self.inputs.get()
        ev = self.event_generator.gen(self.inp)
        if len(ev)>1:
            print(ev[:-1])

        for e in ev:
            if self.next_state is not None:
                break
            self.handler(e)

        if self.next_state:
            self.set_state(self.next_state)
        
        self.outputs.update()

        if DUMMY:
            dummy.update()
    
    def print(self,page):
        page = "".join(str(i) for i in page)

        self.printer.print_smart(open_page(page))

    def run(self):
        while True:
            self.update()
            time.sleep(0.05)


if __name__=="__main__":
    if DUMMY:
        COLORS[BLACK] = (80,80,80)
        BLINKING_COLORS[BLACK] = (80,80,80)
    Machine().run()
