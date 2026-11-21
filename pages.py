
import os
import yaml


class Page:
    def __init__(self,num):
        num=str(num)
        self.num=num
        with open(f"pages/{num}","r") as fp:
            data = fp.read()
            y,contents = data.split("---",1)
            meta = yaml.safe_load(y)
            self.title = meta["title"].strip().upper()
            self.contents = contents.strip().upper()

    def contents_raw(self):
        return self.contents.replace("{","").replace("}","")

    def accessible(self,permissions):
        return True

    def __str__(self):
        return "\n".join([
            f"@~----------- BESTAND: {self.num} -------------~@",
            " "*(len(self.title)//2)+self.title,
            "@~--------------------------------------~@",
            "",
            self.content
        ])
    
    def str(self):
        return str(self)

    def str_err(self,err):
        return "\n".join([
            f"@~----------- BESTAND: {self.num} -------------~@",
            " "*(len(self.title)//2)+self.title,
            "",
            err,
            "@~--------------------------------------~@",
        ])
        




def list_pages():
    return sorted(os.listdir("pages"))

def print_index():
    for p in list_pages():
        page=Page(p)
        print(page.num,page.title)

def check_pages():
    for p in list_pages():
        page=Page(p)
        if len(page.title)>42-len(""):
            print(f"Title of {page.num} too long")
        for line in page.contents_raw().split("\n"):
            if len(line)>42:
                print(f"Line in {page.num} too long ({len(line)}): {line}")

if __name__=="__main__":
    print_index()
    check_pages()
