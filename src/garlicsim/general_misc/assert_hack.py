# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import types

log=[]

class E(Exception):
    def __getattr__(self, a):
        global log
        log.append(a)
        return self.__dict__[a]
'''
OldAssertionError = AssertionError
    
class MyAE(OldAssertionError):    
    def __init__(self, *args):
        if args and isinstance(args[0], BaseException):
            raise args[0]
        else:
            OldAssertionError.__init__(self, *args)

AssertionError = MyAE

assert False, ValueError('shit')
'''

def __init__(self, *args):
    if args and isinstance(args[0], BaseException):
        raise args[0]
    else:
        OldAssertionError.__init__(self, *args)

old_init = AssertionError.__init__

AssertionError.__init__ = types.MethodType(__init__, None, AssertionError)