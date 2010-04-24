# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Settings class.

See its documentation for more info.
'''

import misc

class Settings(object):
    '''A set of settings for a simpack.'''
    # todo: subclass from a pretty vars-shower
    
    def __init__(self):

        self.FORCE_CRUNCHER = None
        '''
        A cruncher that this simpack insists on using.
        
        This is useful because some simpack can't be used with CruncherProcess,
        because of its sometimes-nonstandard behavior.
        '''        
        
        self.DETERMINISM_FUNCTION = misc.default_determinism_function
        '''
        Function that takes a step profile and says whether its deterministic.
        
        What this function says is, "If you do a simulation using this step
        profile, then you will have a deterministic simulation." (Or
        undeterministic, depends on the step profile.)
        
        Note that this function does not return True or False: It returns a
        `DeterminismSetting` class. For details about those, see documentation
        in garlicsim.misc.settings_constants.settings.
        
        The function will return None if it's unknown whether the step profile
        is deterministic.
        '''

        self.SCALAR_STATE_FUNCTIONS = []
        '''
        List of scalar state functions given by the simpack.
        
        A scalar state function is a function from a state to a real number.
        These should be decorated by garlicsim.misc.cached.state_cache.
        '''
        
        self.SCALAR_HISTORY_FUNCTIONS = []
        '''
        List of scalar history functions given by the simpack.
        
        A scalar history function is a function from a history browser to a real
        number. These should be decorated by
        garlicsim.misc.cached.history_cache.
        '''