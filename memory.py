
from random import choice,randint

def random_color(exclude=None):
    return choice([k for k in [1,2,4] if k!=exclude])

def random_pos(n):
    res = [0]*3
    res[randint(0,2)]=n
    return tuple(res)

def random_pos2(a,b):
    return choice([(0,a,b),(b,0,a),(a,b,0)])

def generate():
    code=[None]*5
    
    code[0] = random_pos(random_color())

    code[1] = random_pos(random_color())

    a = random_color()
    b = random_color(a)
    code[2] = random_pos2(a,b)

    code[3] = (random_color(),random_color(),random_color())

    while True:
        code[4] = tuple(choice([0,1,2,4]) for _ in range(3))
        if code[4]==(0,0,0):
            continue

        seen = list(sum(code[:5], start=())) + answer(code[0:4])
        R=seen.count(1)
        G=seen.count(2)
        B=seen.count(4)
        m=max([R,G,B])
        if (R==m)+(G==m)+(B==m) > 1:
            continue
        
        break

    return code

def answer(code):
    ans = [None]*len(code)
    
    if len(code)>=1: #R->G, G->B, B->R
        ans[0] = {1:2,2:4,4:1}[sum(code[0])]
    if len(code)>=2: #1->B, 2->R, 3->G
        ans[1] = {1:4,2:1,4:2}[(code[1][0]!=0)+(code[1][1]!=0)*2+(code[1][2]!=0)*4]
    if len(code)>=3:
        pos0 = (code[0][0]!=0)+(code[0][1]!=0)*2+(code[0][2]!=0)*4
        match pos0:
            case 1:
                match code[2]: #linker
                    case (a,b,0):
                        ans[2]=a
                    case (0,a,b):
                        ans[2]=a
                    case (b,0,a):
                        ans[2]=a
            case 2:
                match code[2]: #rechter
                    case (a,b,0):
                        ans[2]=b
                    case (0,a,b):
                        ans[2]=b
                    case (b,0,a):
                        ans[2]=b
            case 4: #ontbrekend
                ans[2]=[k for k in [1,2,4] if k not in code[2]][0]
    if len(code)>=4:
        match sum(code[1]):
            case 1:
                ans[3]=max([(code[3].count(1),9,1),(code[3].count(2),8,2),(code[3].count(4),7,4)])[2]
            case 2:
                ans[3]=min([(code[3].count(2),7,2),(code[3].count(4),8,4),(code[3].count(1),9,1)])[2]
            case 4:
                cnt=sorted([code[3].count(1),code[3].count(2),code[3].count(4)])[1]
                ans[3]=max([({4:9,1:8,2:7}[k],k) for k in [1,2,4] if code[3].count(k)==cnt])[1]
    if len(code)>=5:
        seen=sum(code,start=())
        R=seen.count(1)
        G=seen.count(2)
        B=seen.count(4)
        ans[4] = {1:4,2:2,4:1}[max([(R,1),(G,2),(B,4)])[1]]
    return ans

if __name__=="__main__":
    for i in range(10):
        c=generate()
        a=answer(c)
        z = ((str(c)+" "+str(a))
             .replace("1","R")
             .replace("2","G")
             .replace("4","B")
             .replace("0","-")
             .replace("R, ","R")
             .replace("G, ","G")
             .replace("B, ","B")
             .replace("-, ","-")
             .replace("(","")
             .replace(")","")
        )
        print(z)

