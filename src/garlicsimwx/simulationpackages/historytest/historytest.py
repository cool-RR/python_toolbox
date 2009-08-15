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


def step(history_browser,*args,**kwargs):

    new_state=garlicsim.state.State()

    with history_browser:
        root=history_browser.request_state_by_number(0)

    if random.choice([True,False]):
        new_state.number=root.number
    else:
        new_state.number=888
    return new_state

step.history_looker=True