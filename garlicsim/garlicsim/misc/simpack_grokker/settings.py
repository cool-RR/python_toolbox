# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Settings` class.

See its documentation for more info.
'''

from . import misc

class Settings(object):
    '''A set of settings for a simpack.'''
    # todo: subclass from a pretty vars-shower
    
    def __init__(self, simpack_grokker):
        
        self.CRUNCHERS = misc.DefaultCRUNCHERS(simpack_grokker)
        '''
        Crunchers that this simpack says it can use.
        
        Crunchers can be specified in different ways. You may specify a
        cruncher type, or the string name of a cruncher type, or a list of
        either of those, or a filter function for cruncher types.
        
        This is useful because some simpacks can't be used with certain kinds
        of crunchers.
        '''
        
        self.DETERMINISM_FUNCTION = misc.default_determinism_function
        '''
        Function that takes a step profile and says whether it's deterministic.
        
        What this function says is, "If you do a simulation using this step
        profile, then you will have a deterministic simulation." (Or
        undeterministic, depends on the step profile.)
        
        This is useful because it allows `garlicsim` to detect if a simulation
        has reached a repititive state, so it can stop the crunching right
        there and avoid wasting resources.

        Note that this function does not return `True` or `False`: It returns a
        `DeterminismSetting` class. For details about those, see documentation
        in `garlicsim.misc.settings_constants.settings`.
        
        The function will return `None` if it's unknown whether the step
        profile is deterministic.
        '''

        self.SCALAR_STATE_FUNCTIONS = []
        '''
        List of scalar state functions given by the simpack.
        
        A scalar state function is a function from a state to a real number.
        It's recommended to decorate these with
        `garlicsim.general_misc.caching.cache`
        '''
        
        self.SCALAR_HISTORY_FUNCTIONS = []
        '''
        List of scalar history functions given by the simpack.
        
        A scalar history function is a function from a history browser to a
        real number. These should be decorated by
        `garlicsim.misc.cached.history_cache`.
        '''