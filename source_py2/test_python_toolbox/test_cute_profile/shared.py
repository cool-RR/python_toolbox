# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines tools for testing `python_toolbox.cute_profile`.'''

import sys

from python_toolbox.sys_tools import OutputCapturer
from python_toolbox import logic_tools

segments = ('function calls in', 'Ordered by', 'ncalls', 'tottime', 'percall',
            'cumtime')


def call_and_check_if_profiled(f):
    '''Call the function `f` and return whether it profiled itself.'''

    with OutputCapturer() as output_capturer:
        f()

    output = output_capturer.output

    segments_found = [(segment in output) for segment in segments]

    if not logic_tools.all_equivalent(segments_found):
        raise Exception("Some segments were found, but some weren't; can't "
                        "know if this was a profiled call or not. Possibly "
                        "some of our segments are wrong.")

    return segments_found[0]


