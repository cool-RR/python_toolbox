# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the ArgumentsProfile class. See its documentation for
more information.
'''

class ArgumentsProfile(object):
    '''
    A profile of *args and **kwargs to be used with a function.
    
    Usage:
    
    arguments_profile = ArgumentsProfile(34, "meow", width=60)
    
    function(*arguments_profile.args, **arguments_profile.kwargs)
    # is equivalent to
    function(34, "meow", width=60)
    
    '''
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def __eq__(self, other):
        return isinstance(other, ArgumentsProfile) and \
               self.args == other.args and self.kwargs == other.kwargs