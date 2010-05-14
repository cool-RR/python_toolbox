

import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    # This is your State subclass. Your state objects should contain all the
    # information there is about a moment of time in your simulation.
    
    def __init__(self):
        pass
    
    
    def step(self):
        # This function is the heart of your simpack. What it does is take an
        # existing world state, and output the next world state.
        #
        # This is where all the crunching gets done. This function defines the
        # laws of your simulation world.
        # 
        # The step function is one of the very few things that your simpack
        # **must** define. Almost all of the other definitions are optional.
        pass
    
        
    @staticmethod
    def create_root():
        # In this function you create a root state. This usually becomes the
        # first state in your simulation. You can make this function do
        # something simple: For example, if you're simulating Life, you can make
        # this function create an empty board.
        #
        # This function may take arguments, if you wish, to be used in making
        # the state. For example, in a Life simulation you may want to specify
        # the width and height of the board using arguments to this function.
        #
        # This function returns the newly-created state.
        pass

    
    @staticmethod
    def create_messy_root():
        # In this function you create a messy root state. This usually becomes the
        # first state in your simulation. 
        #
        # Why messy? Because sometimes you want to have fun in your simulations.
        # You want to create a world where there's a lot of mess, with many
        # objects interacting with each other. This is a good way to test-drive
        # your simulation.
        #
        # This function may take arguments, if you wish, to be used in making
        # the state. For example, in a Life simulation you may want to specify
        # the width and height of the board using arguments to this function.
        #
        # This function returns the newly-created state.
        pass
                                 
    
    # def step_generator(self):
    #     yield None
    #     pass
    #
    # Do you want to use a step generator as your step function? If so, you may
    # uncomment the above and fill it in, and it will be used instead of the
    # normal step function.
    # 
    # A step generator is similar to a regular step function: it takes a
    # starting state, and computes the next state. But it doesn't `return` it,
    # it `yield`s it. And then it doesn't exit, it just keeps on crunching and
    # yielding more states one by one.
    # 
    # A step generator is useful when you want to set up some environment and/or
    # variables when you do your crunching. It can help you save resources,
    # because you won't have to do all that initialization every time garlicsim
    # computes a step.
    #
    # (You may write your step generator to terminate at some point or to never
    # terminate-- Both ways are handled by garlicsim.)
    
    @garlicsim.misc.caching.state_cache
    def get_energy(self):
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
    '''tododoc'''
    try:
        if step_profile.args[1] is True or step_profile.kwargs['krazy'] is True:
            return garlicsim.misc.settings.UNDETERMINISTIC
    except LookupError:
        pass
    
    return garlicsim.misc.settings.DETERMINISTIC