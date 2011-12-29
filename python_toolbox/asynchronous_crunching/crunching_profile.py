# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CrunchingProfile` class.

See its documentation for more information.
'''

import garlicsim.misc


class CrunchingProfile(object):
    '''Instructions that a cruncher follows when crunching the simulation.'''
    
    def __init__(self, clock_target, step_profile):
        '''
        Construct the CrunchingProfile.
        
        `clock_target` is the clock until which we want to crunch.
        `step_profile` is the step profile we want to use.
        '''
        
        self.clock_target = clock_target
        '''We crunch until we get a clock of `.clock_target` or higher.'''

        assert isinstance(step_profile, garlicsim.misc.StepProfile)
        self.step_profile = step_profile
        '''The step profile we want to be used with the step function.'''
  
        
    def state_satisfies(self, state):
        '''
        Check whether a state has a clock high enough to satisfy this profile.
        '''
        return state.clock >= self.clock_target

    
    def raise_clock_target(self, clock_target):
        '''Make `.clock_target` at least as big as the given `clock_target`.'''
        if self.clock_target < clock_target:
            self.clock_target = clock_target
    
            
    def __eq__(self, other):
        return isinstance(other, CrunchingProfile) and \
               self.clock_target == other.clock_target and \
               self.step_profile == other.step_profile

    
    __hash__ = None
    # `CrunchingProfile` is mutable so it should never be hashed.

    
    def __ne__(self, other):
        return not self.__eq__(other)

    
    def __repr__(self):
        '''
        Get a string representation of the crunching profile.
        
        Example output:
        
            CrunchingProfile(clock_target=infinity,
            step_profile=life.State.step(<state>))
        '''
        return 'CrunchingProfile(clock_target=%s, step_profile=%s)' % (
            self.clock_target,
            self.step_profile.__repr__(short_form=True)
        )
        
    
    
    