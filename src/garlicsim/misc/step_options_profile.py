# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StepOptionsProfile class. See its documentation for
more information.
'''

__all__ = ['StepOptionsProfile']

class StepOptionsProfile(object):
    '''
    A profile of *args and **kwargs to be used with a step function.
    
    Usage:
    
    step_options_profile = StepOptionsProfile(34, "meow", width=60)

    step(state, *arguments_profile.args, **arguments_profile.kwargs)
    # is equivalent to
    step(state, 34, "meow", width=60)
    '''
    def __init__(self, *args, **kwargs):
        
        # Perhaps we were passed a StepOptionsProfile object instead of args
        # and kwargs? If so load that one, cause we're all cool and nice.
        candidate = None
        if len(args) == 1 and len(kwargs) == 0:
            candidate = args[0]
        if len(args) == 0 and len(kwargs) == 1 and \
           ('step_options_profile' in kwargs):
            candidate = kwargs['step_options_profile']
        
        if isinstance(candidate, StepOptionsProfile):
            self.__load_from(candidate)
            return
        
        self.args, self.kwargs = args, kwargs
        
        
    def __load_from(profile):
        '''
        Take another step options profile and load its arguments into this one.
        '''
        self.args, self.kwargs = profile.args, profile.kwargs
        
    def __repr__(self):
        args_string = ', '.join([repr(thing) for thing in self.args])
        kwargs_string = ', '.join([str(key)+'='+repr(value) for \
                                   (key, value) in self.kwargs.items()])
        strings = [thing for thing in [args_string, kwargs_string] if \
                   thing]        
        big_string = ', '.join(strings)
        return 'StepOptionsProfile(%s)' % big_string
    
    def __eq__(self, other):
        if other is None:
            return len(self.args) == 0 and len(self.kwargs) == 0
        else:
            return isinstance(other, StepOptionsProfile) and \
                   self.args == other.args and self.kwargs == other.kwargs

    def __ne__(self, other):
        return not self.__eq__(other)