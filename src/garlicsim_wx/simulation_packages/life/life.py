# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

import garlicsim.data_structures
import random

def step(old_state, *args, **kwargs):
    old_board = old_state.board
    new_board = Board(parent=old_board)
    new_state = garlicsim.data_structures.State()
    new_state.board = new_board
    return new_state

def make_plain_state(width=50, height=50, fill="empty"):
    my_state = garlicsim.data_structures.State()
    my_state.board = Board(width, height, fill)
    return my_state

def make_random_state(width=50, height=50):
    my_state = garlicsim.data_structures.State()
    my_state.board = Board(width, height, fill="random")
    return my_state


class Board(object):
    def __init__(self, width=None, height=None, fill="empty", parent=None):
        if parent:
            self.__list = [None] * parent.width * parent.height
            for x in parent.width:
                for y in parent.height:
                    self.set(x, y, parent.cell_will_become(x, y))
            return
                
        assert fill in ["empty", "full", "random"]
        
        if fill == "empty":
            make_cell = lambda: False
        elif fill == "full":
            make_cell = lambda: True
        elif fill == "random":    
            make_cell = lambda: random.choice([True, False])

        self.width, self.height = (width, height)
        self.__list = []
        for i in range(self.width*self.height):
            self.__list.append(make_cell())

    def get(self, x, y):
        return self.__list[ (x % self.width) * self.height + (y%self.height) ]

    def set(self, x, y, value):
        self.__list[ (x%self.width) * self.height + (y%self.height) ] = value

    def get_true_neighbors_count(self, x, y):
        result = 0
        for i in [-1 ,0 ,1]:
            for j in [-1, 0 ,1]:
                if i==j==0:
                    continue
                if self.get(x+i, y+j) is True:
                    result += 1
        return result

    def cell_will_become(self,x,y):
        n = self.get_true_neighbors_count(x, y)
        if self.get(x, y) is True:
            if 2<=n<=3:
                return True
            else:
                return False
        else: # self.get(x, y) is False
            if n==3:
                return True
            else:
                return False

    def __repr__(self):
        return "\n".join(["".join([("#" if self.get(x,y) is True else " ")\
                                   for y in range(self.height)]) for \
                          x in range(self.width)])
