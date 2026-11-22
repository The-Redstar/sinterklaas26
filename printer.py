try:
    from escpos.printer import Usb
except:
    from dummy import Usb

class Printer:
    def __init__(self):
        self.printer = Usb(0x04b8,0x0202)
    def print(self,page):
        self.printer.textln(page.strip())
        self.printer.cut()
    def print_smart(self,page):
        page=page.strip()
        for c in page:
            if c=="{":
                self.printer.set(bold=True)
            elif c=="}":
                self.printer.set(bold=False)
            else:
                self.printer.text(c)
        self.printer.set(bold=False)
        self.printer.ln()
        self.printer.cut()

if __name__=="__main__":
    p = Printer()
    p.print("""
Hello World!
This is a simple print.
    """)
    p.print_smart("""
Hello {World}!

This printing mode supports {bold text} which is quite cool!

    """)
