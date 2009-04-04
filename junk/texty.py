import nibmaster
import string
import random

line=80
tree=nibmaster.nibtree()
root=tree.newnib(touched=True)
root.nib.pos=0
current=root

while True:

    print(string.join(["_"*current.nib.pos,"@","_"*(line-1-current.nib.pos)],""))
    x=raw_input("> ")
    if x[0]=="g":
        newnib=tree.newnib(parent=current)
        newnib.nib.pos=(current.nib.pos+random.choice([-1,1,1,2]))%line
        current=newnib
    elif x[0]=="l":
        y=int(raw_input("How long ago? "))
        for i in range(y):
            current=current.parent


