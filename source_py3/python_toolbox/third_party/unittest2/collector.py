# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import os
import sys
from .loader import defaultTestLoader

def collector():
    # import __main__ triggers code re-execution
    __main__ = sys.modules['__main__']
    setupDir = os.path.abspath(os.path.dirname(__main__.__file__))
    return defaultTestLoader.discover(setupDir)
