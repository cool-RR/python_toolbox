# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StepProfile class.

See its documentation for more information.
'''

import copy

from garlicsim.general_misc import caching
from garlicsim.general_misc.arguments_profile import ArgumentsProfile

from garlicsim.misc.simpack_grokker.get_step_type import get_step_type


__all__ = ['StepProfile']


class StatePlaceholder(object): # tododoc: make uninstanciable
    pass


class StepProfile(ArgumentsProfile):
    '''
    Profile for doing simulation step, specifying step function and arguments.
    
    Using different step profiles, you can crunch your simulation in different
    ways, using different world laws, different contsants and different
    algorithm, within the same project.

    The step profile contains three things:
    
      1. A reference to the step fucntion.
      2. A list of arguments.
      3. A dict of keyword arguments
      
    For example, if you're doing a simulation of Newtonian Mechanics, you can
    create a step profile with `kwargs` of {'G': 3.0} in order to change the
    graviational constant of the simulation on-the-fly.
    '''
    # todo: perhaps this should be based on an ArgumentsProfile after all?
    # In __repr__ and stuff we'll just check self's class. How does Python
    # do it when you subclass its builtin types?

    
    __metaclass__ = caching.CachedType
    
    
    def __init__(self, step_function, *args, **kwargs):
        
        # Perhaps we were passed a StepProfile object instead of args
        # and kwargs? If so load that one, cause we're all cool and nice.
        candidate = None
        if len(args) == 1 and len(kwargs) == 0:
            candidate = args[0]
        if len(args) == 0 and len(kwargs) == 1 and \
           ('step_profile' in kwargs):
            candidate = kwargs['step_profile']
        
        if isinstance(candidate, StepProfile):
            ArgumentsProfile.__init__(self, candidate.step_function,
                                      *((StatePlaceholder,) + candidate.args),
                                      **candidate.kwargs)
        else:
            ArgumentsProfile.__init__(self, step_function,
                                      *((StatePlaceholder,) + args),
                                      **kwargs)

        assert self.args[0] is StatePlaceholder
        self.args = self.args[1:]
        
        self.step_function = self.function
        
        
    @staticmethod
    def build_with_default_step_function(default_step_function, *args,
                                         **kwargs):
        '''
        Create step profile, allowing the user to not specify step function.
        
        Most of the time when simulating, there is one default step function
        that should be used if no other step function was explicitly specified.
        But then again, we also want to allow the user to specify a step
        function if he desires. So we get the (*args, **kwargs) pair from the
        user, and we need to guess whether the user passed in a step function
        for to use, or didn't, and if he didn't we'll use the default one.
        
        The user may put the step function as the first positional argument, or
        as the 'step_function' keyword argument. 
        '''
        # tododoc: it's confusing thinking who should give the
        # `default_step_function`. make this clear in docstring, or possibly
        # make a function that returns a function.

        # We have two candidates to check now: args[0] and
        # kwargs['step_function']. We'll check the kwargs one first, because
        # that's more explicit and there's less chance we'll be catching some
        # other object by mistake.
        #
        # So we start with kwargs:
        
        if 'step_function' in kwargs:
            step_function = kwargs['step_function']
            
            get_step_type(step_function)
            # Just so things will break if it's not a step function. If the user
            # specified 'step_function', he's not going to get away with it not
            # being an actual step function.

            kwargs_copy = kwargs.copy()
            del kwargs_copy['step_function']
            
            return StepProfile(step_function, *args, **kwargs_copy)

        
        # No step function in kwargs. We'll try args:
        
        elif args:
            
            candidate = args[0]
            
            try:
                get_step_type(candidate)
            except Exception:
                return StepProfile(default_step_function, *args, **kwargs)
            else:
                args_copy = args[1:]
                return StepProfile(default_step_function, *args_copy, **kwargs)
        
        else:
            return StepProfile(default_step_function, *args, **kwargs)
                
    
    def __repr__(self):
        '''
        Get a string representation of the step profile.
        
        Example output:
        StepProfile(<unbound method State.step>, 'billinear', t=7)
        '''#tododoc
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