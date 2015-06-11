# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines various functions related to context managers.

See their documentation for more information.
'''

import sys

from .context_manager_type import ContextManagerType


@ContextManagerType
def nested(*managers):
    # Code from `contextlib`
    exits = []
    vars = []
    exc = (None, None, None)
    try:
        for mgr in managers:
            exit = mgr.__exit__
            enter = mgr.__enter__
            vars.append(enter())
            exits.append(exit)
        yield vars
    except:
        exc = sys.exc_info()
    finally:
        while exits:
            exit = exits.pop()
            try:
                if exit(*exc):
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        if exc != (None, None, None):
            # Don't rely on sys.exc_info() still containing
            # the right information. Another exception may
            # have been raised and caught by an exit method
            raise exc[1].with_traceback(exc[2])
    