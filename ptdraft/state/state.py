"""
TODO:
maybe it's silly that a parentless node must be touched?
---
create mechanism for "stitching" nodes(making one a child
of the other artificially)
--
"""

import warnings


class State(object):
    """
    A state in the simulation.

    Most states are untouched, a.k.a. natural, but some states are touched.
    A touched state is a state that was not formed naturally by a simulation step:
    It was created by the user, either from scratch or based on another state.

    I think that a State object must always be serializable - Keep in mind
    when you're giving it attributes. (They should all be serializable.)
    """
    def __init__(self,touched=False):
        self.__touched=touched
    def is_touched(self):
        return self.__touched
    """
    I commented these because I think maybe
    changing the __touched variable should be hard

    def make_touched(self):
        self.__touched=True
    def make_untouched(self):
        self.__touched=False
    """
