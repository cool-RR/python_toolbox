import os
import sys
from python_toolbox.third_party.unittest2.loader import defaultTestLoader

def collector():
    # import __main__ triggers code re-execution
    __main__ = sys.modules['__main__']
    setupDir = os.path.abspath(os.path.dirname(__main__.__file__))
    return defaultTestLoader.discover(setupDir)
