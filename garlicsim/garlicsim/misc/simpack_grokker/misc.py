# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines miscellaneous objects for `simpack_grokker`.'''

def default_determinism_function(step_profile):
    '''
    The default determinism function.
    
    Just returns None, meaning we have no idea whether the step profile is
    deterministic.
    '''
    return None