

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
    
    
