# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StepProfile class.

See its documentation for more information.
'''

import copy

from garlicsim.misc.simpack_grokker.get_step_type import get_step_type


__all__ = ['StepProfile']


class StepProfile(object): # todo: use CachedType?
    '''
    A profile of *args and **kwargs to be used with a step function. tododoc
    '''
    # todo: perhaps this should be based on an ArgumentsProfile after all?
    # In __repr__ and stuff we'll just check self's class. How does Python
    # do it when you subclass its builtin types?
    
    def __init__(self, step_function, *args, **kwargs):
        
        assert callable(step_function)
        self.step_function = step_function
        
        # Perhaps we were passed a StepProfile object instead of args
        # and kwargs? If so load that one, cause we're all cool and nice.
        candidate = None
        if len(args) == 1 and len(kwargs) == 0:
            candidate = args[0]
        if len(args) == 0 and len(kwargs) == 1 and \
           ('step_profile' in kwargs):
            candidate = kwargs['step_profile']
        
        if isinstance(candidate, StepProfile):
            self.__load_from(candidate)
            return
        
        self.args = tuple(args)
        self.kwargs = kwargs  # todo: Get some frozendict class for this
        
        
    def __load_from(self, profile):
        '''
        Take another step options profile and load its arguments into this one.
        '''
        self.step_function = step_profile.step_function
        self.args = copy.copy(step_profile.args)
        self.kwargs = copy.copy(step_profile.kwargs)
        
 
    @staticmethod
    def build_with_default_step_function(default_step_function, *args,
                                         **kwargs):
    
        # Notice how we take from kwargs first.
        candidates = None
        if 'step_function' in kwargs:
            candidates.append(kwargs['step_function'])
        if len(args) >= 1:
            candidates.append(args[0])
            
        if 'step_function' in kwargs:
            step_function = kwargs['step_function']
            
            get_step_type(step_function)
            # Just so things will break if it's not a step function.

            kwargs_copy = kwargs.copy()
            del kwargs_copy['step_function']
            
            return StepProfile(step_function, *args, **kwargs)

        
        elif args:
            
            candidate = args[0]
            
            try:
                get_step_type(candidate)
            except Exception:
                return StepProfile(default_step_function, *args, **kwargs)
            else:
                args_copy = args[1:]
                return StepProfile(default_step_function, *args_copy, **kwargs)
        
        return StepProfile(default_step_function, *args, **kwargs)
                
    
    def __repr__(self):
        '''
        Get a string representation of the step profile.
        
        Example output:
        StepProfile(<unbound method State.step>, 'billinear', t=7)
        '''
        args_string = ', '.join(
            [repr(thing) for thing in (self.step_function,) + self.args]
        )
        kwargs_string = ', '.join([str(key)+'='+repr(value) for \
                                   (key, value) in self.kwargs.items()])
        strings = [thing for thing in [args_string, kwargs_string] if \
                   thing]        
        big_string = ', '.join(strings)
        return 'StepProfile(%s)' % big_string
    
    
    def __eq__(self, other):
        return isinstance(other, StepProfile) and \
               self.step_function is other.step_function and \
               self.args == other.args and self.kwargs == other.kwargs

    
    def __hash__(self):
        # Defining __hash__ because there's __eq__ which makes the default
        # __hash__ disappear on Python 3.
        return id(self)

    
    def __ne__(self, other):
        return not self.__eq__(other)