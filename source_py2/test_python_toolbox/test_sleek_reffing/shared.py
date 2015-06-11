# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for testing `python_toolbox.sleek_reffing`.'''

import weakref

from python_toolbox import misc_tools


def _is_weakreffable(thing):
    '''Return whether a weakref can be created to `thing`.'''
    try:
        weakref.ref(thing)
    except TypeError:
        return False
    else:
        return True

    
class A(object):
    '''A class with a static method.'''
    @staticmethod
    def s():
        pass

    
@misc_tools.set_attributes(count=0)
def counter(*args, **kwargs):
    '''Function that returns a higher number every time it's called.'''
    try:
        return counter.count
    finally:
        counter.count += 1
