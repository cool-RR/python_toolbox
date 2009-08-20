import garlicsim.state
import copy

import math
from math import pi
import random
random.seed()
def make_plain_state(*args, **kwargs):
    state=garlicsim.state.State()
    state._State__touched = True
    state.left = 0
    state.left_vel = 0
    state.right = 0
    return state


def make_random_state(*args, **kwargs):
    state=garlicsim.state.State()
    state._State__touched = True
    state.left = random.random() * 2 * pi
    state.left_vel = 0
    state.right = random.random() * 2 * pi
    return state


def history_step(history_browser, *args, **kwargs):

    last_state = history_browser.get_last_state()
    new_state = copy.deepcopy(last_state)
    new_state.clock += 1
    new_state._State__touched = False
    
    new_state.left_vel += random.random() * 0.2 - 0.1
    new_state.left += new_state.left_vel
    
    past_state = history_browser.request_state_by_clock(new_state.clock - 20)
    if past_state is not None:
        new_state.right = past_state.left
        
    return new_state
