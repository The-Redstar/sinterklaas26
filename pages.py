
import os
import yaml

FILE_HEADER_START = "{{@=-----------: BESTAND: {n} :-----------=@}}"
FILE_HEADER_END   =  "{@=--------------------------------------=@}"

class Page:
    def __init__(self,num):
        self.num=num

        with open(f"pages/{num}","r") as fp:
            data = fp.read()
            y,contents = data.split("---",1)
            meta = yaml.safe_load(y)
            self.title = meta["title"].strip().upper()
            self.content = contents.strip().upper()


    def contents_raw(self):
        return self.content.replace("{","").replace("}","")

    def accessible(self,permissions):
        return True

    def __str__(self):
        return "\n".join([
            FILE_HEADER_START.format(n=self.num[:3]),
            " "*(21-len(self.title)//2)+"{"+self.title+"}",
            FILE_HEADER_END,
            "",
            self.content
        ])
    
    def str(self):
        return str(self)

    def str_msg(self):
        return "\n".join([
            FILE_HEADER_START.format(n=self.num[:3]) if self.num else FILE_HEADER_END,
            " "*(len(self.title)//2)+self.title,
            "",
            self.content,
            FILE_HEADER_END,
        ])
        
class MsgPage(Page):
    def __init__(self,num,title,msg):
        self.num=num
        self.title=title
        self.content=msg


def open_page(num):
    if os.path.exists("pages/"+num):
        return Page(num).str()
    else:
        return MsgPage(num,"ERROR","{404:} bestand niet gevonden").str_msg()

def list_pages():
    return sorted(os.listdir("pages"))

def print_index():
    for p in list_pages():
        page=Page(p)
        print(page.num,page.title)

def check_pages():
    for p in list_pages():
        page=Page(p)
        print(page.num,page.title)
        if len(page.title)>42-len(""):
            print(f"  Title of {page.num} too long")
        if "TODO" in page.content:
            print(f"  Found TODO in {page.num}")
        for line in page.contents_raw().split("\n"):
            if len(line)>42:
                print(f"  Line in {page.num} too long ({len(line)}): {line}")
            if "\t" in line:
                print(f"  Tab in {page.num} in line {line}")

if __name__=="__main__":
    #print_index()
    check_pages()
