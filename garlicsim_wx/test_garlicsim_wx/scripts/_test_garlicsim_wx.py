#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Script for launching `garlicsim_wx` tests when installed in local Python.'''


import test_garlicsim_wx


if __name__ == '__main__':
    test_garlicsim_wx.invoke_nose()