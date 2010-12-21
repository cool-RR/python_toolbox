# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines tools for testing `garlicsim.general_misc.cute_profile`.'''

from __future__ import with_statement

import sys

from garlicsim.general_misc.sys_tools import OutputCapturer
from garlicsim.general_misc import logic_tools

segments = ('function calls in', 'Ordered by', 'ncalls', 'tottime', 'percall',
            'cumtime')


def call_and_check_if_profiled(f):
    '''Call the function `f` and return whether it profiled itself.'''
    
    with OutputCapturer() as output_capturer:
        f()
    
    output = output_capturer.output
        
    segments_found = [(segment in output) for segment in segments]
    
    if not logic_tools.all_equal(segments_found):
        raise Exception("Some segments were found, but some weren't; Can't "
                        "know if this was a profiled call or not. Possibly "
                        "some of our segments are wrong.")
    
    return segments_found[0]
    
    
    