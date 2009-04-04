#import ptdraft.nib
#from nib import Nib
import nib
import random
from .core import Simulation


class Life(Simulation):
    """
    """

    def step(self,sourcenib,*args,**kwargs):
        oldboard=sourcenib.board
        newboard=Board(oldboard.width,oldboard.height)
        for x in range(oldboard.width):
            for y in range(oldboard.height):
                newboard.set(x,y,oldboard.willbecome(x,y))
        newnib=nib.Nib()
        newnib.board=newboard
        return newnib

    def makeplainnib(self,width=50,height=50):
        mynib=nib.Nib()
        mynib.board=Board(width,height,False)
        return mynib

    def makerandomnib(self,width=50,height=50):
        mynib=nib.Nib()
        mynib.board=Board(width,height,True)
        return mynib

    def show(self,nib):
        pass



class Board(object):
    def __init__(self,width,height,makerandom=False):
        (self.width,self.height)=(width,height)
        self.__list=[]
        for i in range(self.width*self.height):
            self.__list.append(False if makerandom==False else random.choice([True,False]))
    def get(self,x,y):
        return self.__list[(x%self.width)*self.height+(y%self.height)]
    def set(self,x,y,value):
        self.__list[(x%self.width)*self.height+(y%self.height)]=value
    def getneighbourcount(self,x,y):
        result=0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==j==0:
                    continue
                if self.get(x+i,y+j)==True:
                    result+=1
        return result
    def willbecome(self,x,y):
        n=self.getneighbourcount(x,y)
        if self.get(x, y)==True:
            if 2<=n<=3:
                return True
            else:
                return False
        else: # self.get(x, y)==False
            if n==3:
                return True
            else:
                return False
    def __repr__(self):
        return "\n".join(["".join([("#" if self.get(x,y)==True else " ") for y in range(self.height)]) for x in range(self.width)])


