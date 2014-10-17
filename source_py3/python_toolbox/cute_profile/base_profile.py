# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Wraps the `cProfile` module, fixing a little bug in `runctx`.
'''

from cProfile import *

from .pstats_troubleshooting import troubleshoot_pstats
troubleshoot_pstats()
del troubleshoot_pstats


def runctx(statement, globals, locals, filename=None, sort=-1):
    """Run statement under profiler, supplying your own globals and locals,
    optionally saving results in filename.

    statement and filename have the same semantics as profile.run
    """
    prof = Profile()
    result = None
    try:
        try:
            prof = prof.runctx(statement, globals, locals)
        except SystemExit:
            pass
    finally:
        if filename is not None:
            prof.dump_stats(filename)
        else:
            result = prof.print_stats(sort)
    return result

