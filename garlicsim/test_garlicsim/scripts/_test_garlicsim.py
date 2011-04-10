#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Script for launching `garlicsim` tests when installed in local Python.'''


import test_garlicsim


if __name__ == '__main__':
    test_garlicsim.invoke_nose()