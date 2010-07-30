# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the BaseCruncher class.

See its documentation for more information. See the `crunchers` package for a
collection of crunchers.
'''

import copy

from garlicsim.general_misc.third_party import abc



class BaseCruncher(object):
    '''
    
    '''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        self.crunching_manager = crunching_manager
        self.project = crunching_manager.project
        self.initial_state = initial_state
        self.crunching_profile = copy.deepcopy(crunching_profile)
        
    
    