# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines miscellaneous objects for `simpack_grokker`.'''


def default_determinism_function(step_profile):
    '''
    The default determinism function.
    
    Just returns `None`, meaning we have no idea whether the step profile is
    deterministic.
    '''
    return None


class DefaultCRUNCHERS(object):
    '''The default `CRUNCHERS` setting, which just asks the simpack grokker.'''
    def __init__(self, simpack_grokker):
        self.simpack_grokker = simpack_grokker
    def __call__(self, cruncher_type):
        return cruncher_type.can_be_used_with_simpack_grokker(
            self.simpack_grokker
        )

