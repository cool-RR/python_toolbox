# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A module for simulating Conway's Game of Life.'''

import garlicsim.data_structures
import random

class State(garlicsim.data_structures.State):
    def __repr__(self):
        return self.board.__repr__()
    def __eq__(self, other):
        return isinstance(other, State) and self.board == other.board
    def __ne__(self, other):
        return not self.__eq__(other)
    
def step(old_state, useless=None, krazy=None):
    old_board = old_state.board
    new_board = Board(parent=old_board)
    new_state = State()
    if krazy:
        new_state.board = \
            Board(old_board.width, old_board.height, fill='random')
        return new_state
    new_state.board = new_board
    return new_state

def make_plain_state(width=45, height=25, fill="empty"):
    my_state = State()
    my_state.board = Board(width, height, fill)
    return my_state

def make_random_state(width=45, height=25):
    my_state = State()
    my_state.board = Board(width, height, fill="random")
    return my_state

class Board(object):
    '''
    Represents a Life board.
    ''' 
    def __init__(self, width=None, height=None, fill="empty", parent=None):
        '''
        If `parent` is specified, makes a board which is descendent from the
        parent.
        '''
        if parent:
            assert width == height == None
            self.width, self.height = (parent.width, parent.height)
            self.__list = [None] * parent.width * parent.height
            for x in xrange(parent.width):
                for y in xrange(parent.height):
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
        for i in xrange(self.width*self.height):
            self.__list.append(make_cell())

    def get(self, x, y):
        '''
        Get the value of cell (x, y) in the board.
        '''
        return self.__list[ (x % self.width) * self.height + (y%self.height) ]

    def set(self, x, y, value):
        '''
        Set the value of cell (x, y) in the board to the specified value.
        '''
        self.__list[ (x%self.width) * self.height + (y%self.height) ] = value

    def get_true_neighbors_count(self, x, y):
        '''
        Get the number of True neighbors a cell has.
        '''
        result = 0
        for i in [-1 ,0 ,1]:
            for j in [-1, 0 ,1]:
                if i==j==0:
                    continue
                if self.get(x+i, y+j) is True:
                    result += 1
        return result

    def cell_will_become(self, x, y):
        '''
        Return what value a specified cell will have after an iteration of the
        simulation.
        '''
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
        '''
        Display the board, ASCII-art style.
        '''
        cell = lambda x, y: "#" if self.get(x, y) is True else " "
        row = lambda y: "".join(cell(x, y) for x in xrange(self.width))
        return "\n".join(row(y) for y in xrange(self.height))
    
    def __eq__(self, other):
        return isinstance(other, Board) and self.__list == other.__list
    
    def __ne__(self, other):
        return not self.__eq__(other)

@garlicsim.misc.memoization.state_memoize
def live_cells(state):
    '''Return how many live cells there are in the state.'''
    print('calculating for state %s' % id(state))
    return state.board._Board__list.count(True)

   
for i in range(3):
    states = [node.state for node in path]
    print([live_cells(state) for state in states[-3:]])

@garlicsim.misc.memoization.history_memoize
def changes(history_browser):
    '''
    Return how many cells changed between the most recent state and its parent.
    '''
    try:
        state = history_browser[-1]
        last_state = history_browser[-2]
    except IndexError:
        return None
    board, last_board = state.board, last_state.board
    board_size = len(board._Board__list)
    counter = 0
    for i in xrange(board_size):
        if board._Board__list[i] != last_board._Board__list[i]:
            counter += 1
    return counter

