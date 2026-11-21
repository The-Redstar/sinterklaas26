

class Page:
    def __init__(self,num):
        num=str(num)
        self.num=num
        with open(f"pages/{num}","r") as fp:
            ...
            self.title = None

    def accessible(self,permissions):
        ...

    def __str__(self):
        ...
    
    def print(self):
        return str(self)
        
    def print_err(self,err):
        ...

def list_pages():
    ...

def print_index():
    ...

def check_pages():
    ...

if __name__=="__main__":
    print_index()
    check_pages()
