# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines settings.'''

class Setting(object):
    '''
    A setting.
    
    These are used as classes without insantiating.
    '''

class DeterminismSetting(Setting):
    '''
    A setting of determinism.
    
    When GarlicSim knows that a certain step profile is deterministic, it can
    help it analyze the simulation. For example, it lets GarlicSim detect when
    the simulation has reached a constant/repetitive state.
    '''

class UNDETERMINISTIC(DeterminismSetting):
    '''Completely not deterministic -- has a random element.'''

class SUPPOSEDLY_DETERMINISTIC(DeterminismSetting):
    '''
    Means deterministic in principle, but not absolutely.
    
    For example, in some simpacks rounding errors may make states that should
    otherwise be equal not be equal.
    '''
    # todo: possibly rename, use thesaurus

class DETERMINISTIC(DeterminismSetting):
    '''
    Absolutely deterministic.
    
    There is no random or fuzzy element in the step function, and given
    identical input states it is guaranteed to return identical output states.
    '''

