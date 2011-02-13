#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Script for launching `garlicsim_wx` tests when installed in local Python.'''


import test_garlicsim_wx


if __name__ == '__main__':
    test_garlicsim_wx.invoke_nose()