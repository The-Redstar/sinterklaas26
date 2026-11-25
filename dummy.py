from tkinter import *
import types

from pins import *

from math import sin,cos,pi

class Dummy:
    def __init__(self):
        self.buttons={p:False for p in INPUT_PINS}

        self.servo_angle = 0
        self.rgb=[(0,0,0)]*3
        self.outputs={p:False for p in OUTPUT_PINS}

        self.printing = False
        self.print_n=0
        self.bold=False

        self.root=Tk()
        def widget(row,col,txt="",**gargs):
            w = Label(self.root,width=6,height=3,text=txt)
            w["relief"] = RAISED
            w.grid(row=row,column=col,**gargs)
            return w
        
        self.b1=widget(8,3,"(W)")
        self.b2=widget(8,5,"(E)")
        self.b3=widget(8,7,"(R)")
        self.b1["bg"]="red"
        self.b2["bg"]="red"
        self.b3["bg"]="red"
        self.b4=widget(8,1,"(Q)")
        self.b4["bg"]="lime"
        self.b5=widget(8,9,"[ T ]")
        self.k=widget(2,8,"KEY {K}",columnspan=2)
        self.k["height"]=6
        self.k["width"]=12
        self.lo=widget(8,11,"LO {H}")
        self.hi=widget(7,11,"HI {Y}")
        self.lo["bg"]="#aaa"
        self.hi["bg"]="#aaa"

        self.l1=widget(6,3)
        self.l2=widget(6,5)
        self.l3=widget(6,7)

        self.i1=widget(3,9)
        self.i2=widget(4,9)
        self.i3=widget(5,9)

        widget(8,2)["relief"]=FLAT
        widget(8,4)["relief"]=FLAT
        widget(8,6)["relief"]=FLAT
        widget(8,8)["relief"]=FLAT
        widget(8,10)["relief"]=FLAT

        self.servo=Canvas(self.root,width=250,height=200,relief=RIDGE,borderwidth=3)
        self.servo.grid(row=2,column=1,columnspan=6,rowspan=3)

        Label(self.root,fg="white",bg="purple",text="DRUK/TIJD").grid(row=1,column=2,columnspan=3,sticky=E+W)
        Label(self.root,fg="white",bg="purple",text="SLEUTEL").grid(row=1,column=8,columnspan=2,sticky=E+W)

        Label(self.root,fg="white",bg="purple",text="STOOM").grid(row=3,column=8,columnspan=1,sticky=E+W)
        Label(self.root,fg="white",bg="purple",text="GEHEUGEN").grid(row=4,column=7,columnspan=2,sticky=E+W)
        Label(self.root,fg="white",bg="purple",text="IDENTIFICATIE").grid(row=5,column=6,columnspan=3,sticky=E+W)

        Label(self.root,fg="white",bg="purple",text="OK").grid(row=7,column=1,sticky=E+W+S)
        Label(self.root,fg="white",bg="red",text="1").grid(row=7,column=3,sticky=E+W+S)
        Label(self.root,fg="white",bg="green",text="2").grid(row=7,column=5,sticky=E+W+S)
        Label(self.root,fg="white",bg="blue",text="4").grid(row=7,column=7,sticky=E+W+S)
        Label(self.root,fg="white",bg="gold",text="5 DEC").grid(row=7,column=9,sticky=E+W+S)

        self.root.bind("<KeyPress>",self.press)
        self.root.bind("<KeyRelease>",self.release)


    def update(self):
        # rgb
        self.l1["bg"]="#{:02X}{:02X}{:02X}".format(*self.rgb[0])
        self.l2["bg"]="#{:02X}{:02X}{:02X}".format(*self.rgb[1])
        self.l3["bg"]="#{:02X}{:02X}{:02X}".format(*self.rgb[2])

        # leds
        green = lambda c: "green" if c else "#555"
        self.i1["bg"]=green(self.outputs[PIN_I1])
        self.i2["bg"]=green(self.outputs[PIN_I2])
        self.i3["bg"]=green(self.outputs[PIN_I3])

        self.b5["bg"]="red" if self.outputs[PIN_B5_I] else "#555"

        # servo angle
        self.servo.delete("all")
        dx=125*cos(self.servo_angle/180*pi)
        dy=125*sin(self.servo_angle/180*pi)
        self.servo.create_line(125,200,125+dx,200-dy)

        # button presses
        relief = lambda c: SUNKEN if c else RAISED
        self.b1["relief"] = relief(self.buttons[PIN_B1])
        self.b2["relief"] = relief(self.buttons[PIN_B2])
        self.b3["relief"] = relief(self.buttons[PIN_B3])
        self.b4["relief"] = relief(self.buttons[PIN_B4])
        self.b5["relief"] = relief(self.buttons[PIN_B5])
        self.k["relief"] = relief(self.buttons[PIN_K ])
        self.lo["relief"] = relief(self.buttons[PIN_LO])
        self.hi["relief"] = relief(self.buttons[PIN_HI])

        self.root.update()

    def press(self,e):
        match e.keysym:
            case "1" | "w":
                self.buttons[PIN_B1]=True
            case "2" | "e":
                self.buttons[PIN_B2]=True
            case "3" | "r":
                self.buttons[PIN_B3]=True
            case "4" | "q":
                self.buttons[PIN_B4]=True
            case "5" | "t":
                self.buttons[PIN_B5]=True
            case "6" | "k":
                self.buttons[PIN_K ]=True
            case "7" | "h":
                self.buttons[PIN_LO]=True
            case "8" | "y":
                self.buttons[PIN_HI]=True
    def release(self,e):
        match e.keysym:
            case "1" | "w":
                self.buttons[PIN_B1]=False
            case "2" | "e":
                self.buttons[PIN_B2]=False
            case "3" | "r":
                self.buttons[PIN_B3]=False
            case "4" | "q":
                self.buttons[PIN_B4]=False
            case "5" | "t":
                self.buttons[PIN_B5]=False
            case "6" | "k":
                self.buttons[PIN_K ]=False
            case "7" | "h":
                self.buttons[PIN_LO]=False
            case "8" | "y":
                self.buttons[PIN_HI]=False


    def print(self,txt):
        if not self.printing:
            print("+-"+"-"*42+"-+")
            self.printing = True

        for c in txt:
            if self.print_n==0:
                print("| ",end="")

            if c=="\n":
                print(" "*(42-self.print_n),end="\033[0m |\n")
                self.print_n=0
            else:
                if self.bold:
                    print("\033[1m",end="")
                else:
                    print("\033[0m",end="")
                print(c,end="")
                self.print_n+=len(c)

    def set_bold(self,bold):
        self.bold=bold

    def cut(self):
        self.print("\n")
        print("+-"+"-"*42+"-+")
        self.printing = False
        self.print_n = 0
    
    def input(self,pin):
        x = self.buttons[pin]
        if pin==PIN_HI:
            x = not x
        if x:
            return GPIO.LOW
        return GPIO.HIGH
    
    def output(self,pin,val):
        self.outputs[pin]=val
        

dummy=Dummy()



GPIO = types.SimpleNamespace(
    setmode = lambda x: None,
    setup = lambda p, m, **k: None,
    input = dummy.input,
    output = dummy.output,
    PUD_UP = None,
    LOW = 0,
    HIGH = 1,
    BCM = None,
    IN = None,
    OUT = None,
)


def PiGPIOFactory():
    return None

class AngularServo:
    def __init__(self,*args,**kwargs):
        self._angle=0
    
    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self,val):
        self._angle = val
        dummy.servo_angle = val

class PixelStrip:
    def __init__(self,*args,**kwargs):
        self.colors=[(0,0,0),(0,0,0),(0,0,0)]
    def begin(self):
        pass
    def setPixelColor(self,i,c):
        self.colors[i]=c
    def show(self):
        dummy.rgb=self.colors[:]

def Color(r,g,b):
    return (r,g,b)

class Usb:
    def __init__(self,_a,_b):
        pass
    def text(self,t):
        dummy.print(t)
    def textln(self,t):
        dummy.print(t+"\n")
    def ln(self):
        dummy.print("\n")
    def cut(self):
        dummy.cut()
    def set(self,bold=None,**kwargs):
        if bold is not None:
            dummy.set_bold(bold)
        


