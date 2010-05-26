# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A module for simulating Conway's Game of Life.'''

import random
import itertools

import garlicsim.data_structures


class State(garlicsim.data_structures.State):

    @staticmethod
    def create_diehard(width=45, height=25):
        '''
        Create the Diehard Metushelah.
        
        It looks like this:
        
                   #
             ##
              #   ###

        '''
        state = State()
        state.board = Board.create_diehard(width, height)
        return state
    
    @staticmethod
    def create_root(width=45, height=25, fill='empty'):
        state = State()
        state.board = Board(width, height, fill)
        return state

    
    @staticmethod
    def create_messy_root(width=45, height=25):
        return State.create_root(width, height, fill='random')
                                 
    
    def step(self, useless=None, krazy=None):
        number_of_live_cells = self.get_n_live_cells()
        if number_of_live_cells < (self.board.width * self.board.height) / 10.:
            raise garlicsim.misc.WorldEnd
            
        old_board = self.board        
        new_board = Board(parent=old_board)
        new_state = State()
        if krazy:
            new_state.board = \
                Board(old_board.width, old_board.height, fill='random')
            return new_state
        new_state.board = new_board
        return new_state

    
    @garlicsim.misc.caching.state_cache
    def get_n_live_cells(self):
        '''Return how many live cells there are in the board.'''
        return self.board._Board__list.count(True)

    def __repr__(self):
        return self.board.__repr__()
    
    def __eq__(self, other):
        return isinstance(other, State) and self.board == other.board
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __sub__(self, other): # experimental, test
        if isinstance(other, State):
            return sum(
                (x-y) for (x, y) in itertools.izip(
                    self.board._Board__list,
                    other.board._Board__list
                )
            )
                
        else:
            return NotImplemented
            
    


class Board(object):
    '''Represents a Life board.''' 
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

    @staticmethod
    def create_diehard(width=45, height=25):
        board = Board(width, height)
        (x, y) = (width//2, height//2)
        for (i, j) in [(6, 0), (0, 1), (1, 1), (1, 2), (5, 2), (6, 2), (7, 2)]:
            board.set(x + i, y + j, True)
            
        return board
        
    
    def get(self, x, y):
        '''Get the value of cell (x, y) in the board.'''
        return self.__list[ (x % self.width) * self.height + (y%self.height) ]

    def set(self, x, y, value):
        '''Set the value of cell (x, y) in the board to the specified value.'''
        self.__list[ (x%self.width) * self.height + (y%self.height) ] = value

    def get_true_neighbors_count(self, x, y):
        '''Get the number of True neighbors a cell has.'''
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
        '''Display the board, ASCII-art style.'''
        cell = lambda x, y: "#" if self.get(x, y) is True else " "
        row = lambda y: "".join(cell(x, y) for x in xrange(self.width))
        return "\n".join(row(y) for y in xrange(self.height))
    
    def __eq__(self, other):
        return isinstance(other, Board) and self.__list == other.__list
    
    def __ne__(self, other):
        return not self.__eq__(other)


   

@garlicsim.misc.caching.history_cache
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

def determinism_function(step_profile):
    try:
        if step_profile.args[1] is True or step_profile.kwargs['krazy'] is True:
            return garlicsim.misc.settings.UNDETERMINISTIC
    except LookupError:
        pass
    
    return garlicsim.misc.settings.DETERMINISTIC