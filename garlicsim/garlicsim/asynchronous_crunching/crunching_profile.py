# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the CrunchingProfile class. See its documentation for more
information.
'''

__all__ = ['CrunchingProfile']

class CrunchingProfile(object):
    '''
    A crunching profile is a set of instructions that a cruncher follows when
    crunching the simulation.
    '''
    def __init__(self, clock_target=None, step_profile=None):
        
        self.clock_target = clock_target
        '''
        This says we want the cruncher to crunch until it gets a state with a
        clock of `.clock_target` or higher.
        '''
        
        self.step_profile = step_profile
        '''
        The step options profile we want to be used with the step function.
        '''
  
    def state_satisfies(self, state):
        '''
        Check whether a state has a clock high enough to satisfy this profile.
        '''
        return state.clock >= self.clock_target
    
    def raise_clock_target(self, clock_target): #todo: use this everywhere
        '''
        If .clock_target is lower than the given clock_target, raise it.
        '''
        if self.clock_target < clock_target:
            self.clock_target = clock_target
    
    def __eq__(self, other):
        return isinstance(other, CrunchingProfile) and \
               self.clock_target == other.clock_target and \
               self.step_profile == other.step_profile

    def __hash__(self):
        # Defining __hash__ because there's __eq__ which makes the default
        # __hash__ disappear on Python 3.
        return id(self)

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        stuff = []
        stuff.append("clock_target=%s" % self.clock_target)
        stuff.append("step_profile=%s" % self.step_profile)
        temp = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % temp)
    
    
    
    
    