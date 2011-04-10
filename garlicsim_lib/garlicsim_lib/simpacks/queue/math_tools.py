# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines various mathematical tools.'''

from __future__ import division

import random

def time_for_next_occurence(mean_time_for_next_occurence):
    '''
    Given a mean time between occurences, generate the time for next occurence.
    
    Only for occurences that obey a Poisson distribution.
    '''
    return random.expovariate(1 / mean_time_for_next_occurence)


 