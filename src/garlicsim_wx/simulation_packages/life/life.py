import garlicsim.state
import random
import warnings

#import psyco
#psyco.full()

def step(sourcestate,*args,**kwargs):
    oldboard=sourcestate.board
    newboard=Board(oldboard.width,oldboard.height)
    for x in range(oldboard.width):
        for y in range(oldboard.height):
            newboard.set(x,y,oldboard.will_become(x,y))
    newstate=garlicsim.state.State()
    newstate.board=newboard
    return newstate


def make_plain_state(width=50,height=50,fill="empty"):
    mystate=garlicsim.state.State()
    mystate.board=Board(width,height,fill)
    return mystate

def make_random_state(width=50,height=50):
    mystate=garlicsim.state.State()
    mystate.board=Board(width,height,fill="random")
    return mystate



class Board(object):
    def __init__(self,width,height,fill="empty"):
        assert fill in ["empty","full","random"]

        def make_cell():
            if fill=="empty": return False
            if fill=="full": return True
            if fill=="random": return random.choice([True,False])

        (self.width,self.height)=(width,height)
        self.__list=[]
        for i in range(self.width*self.height):
            self.__list.append(make_cell())

    def get(self,x,y):
        return self.__list[(x%self.width)*self.height+(y%self.height)]

    def set(self,x,y,value):
        self.__list[(x%self.width)*self.height+(y%self.height)]=value

    def get_neighbour_count(self,x,y):
        result=0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==j==0:
                    continue
                if self.get(x+i,y+j)==True:
                    result+=1
        return result

    def will_become(self,x,y):
        n=self.get_neighbour_count(x,y)
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


