import garlicsim.state
import copy
#from garlicsim.misc.myprint import my_print

import random
random.seed()

def make_plain_state(*args,**kwargs):
    state=garlicsim.state.State()
    state._State__touched=True
    state.number=0
    return state


def make_random_state(*args,**kwargs):
    state=garlicsim.state.State()
    state._State__touched=True
    state.number=random.randint(0,10)
    return state


def history_step(history_browser,*args,**kwargs):

    new_state=garlicsim.state.State()
    
    

    with history_browser:
        try:
            root = history_browser[7]
        except IndexError:
            root = history_browser[0]

    if random.choice([True,False]):
        new_state.number=root.number
    else:
        new_state.number=888
    return new_state
