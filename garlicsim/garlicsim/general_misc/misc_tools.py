# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines miscellaneous tools.'''

import re
import math
import types

from . import import_tools


def frange(start, finish=None, step=1.):
    '''
    Make a list containing an arithmetic progression of numbers.

    This is an extension of the builtin `range`; It allows using floating point
    numbers.
    '''
    if finish is None:
        finish, start = start, 0.
    else:
        start = float(start)

    count = int(math.ceil(finish - start)/step)
    return (start + n*step for n in range(count))
    

def getted_vars(thing, _getattr=getattr):
    # todo: can make "fallback" option, to use value from original `vars` if get
    # is unsuccessful.
    my_vars = vars(thing)
    return dict((name, _getattr(thing, name)) for name in my_vars.iterkeys())



_ascii_variable_pattern = re.compile('^[a-zA-Z_][0-9a-zA-Z_]*$')
def is_legal_ascii_variable_name(name):    
    return bool(_ascii_variable_pattern.match(name))
    