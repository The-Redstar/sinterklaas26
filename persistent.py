
# persistent state

import os

FOLDER = "persistent/"

STEAM_COMPLETED="STOOMTEST"
MEMORY_COMPLETED="GEHEUGENTEST"
KEY_COMPLETED="SLEUTELTEST"
START_TIME="START"

class Persistent:
    def __init__(self):
        self.fields = {}
        for file in os.listdir(FOLDER):
            with open(FOLDER+file","r") as fp:
                val = fp.read()
            self.fields[file]=val
    def set(self,key,val=""):
        key=key.upper()
        self.fields[key]=val
        with open(FOLDER+key,"w") as fp:
            fp.write(val)
    def remove(self,key):
        key=key.upper()
        try:
            self.fields.remove(key)
            os.remove(FOLDER+key)
        except:
            pass
    def has(self,key):
        return key.upper() in self.fields
    def get(self,key):
        return self.fields.get(key.upper())

if __name__=="__main__":
    p=Persistent()
    for key in p.fields:
        print(key,p.get(key))
    if input("Clear all? [y/N]")=="y":
        print("Clearing all")
        keys=list(p.fields.keys())
        for k in keys:
            p.remove(k)
