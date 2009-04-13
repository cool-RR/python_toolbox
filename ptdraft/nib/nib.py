"""
TODO:
maybe nibs and nibnodes are redundant? maybe merge them?
---
maybe it's silly that a parentless nibnode must be touched?
---
create mechanism for "stitching" nibleaves (making one a child
of the other artificially)
--
What to do with paths???
--
"""

import warnings


class Nib(object):
    """
    A nib is something like a time-point. It's something like a frozen state of the simulation.

    Most nibs are not touched, but some nibs are touched.
    A touched nib is a nib that was not formed naturally by a simulation step:
    It was created by the user, either from scratch or based on an untouched nib.
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
