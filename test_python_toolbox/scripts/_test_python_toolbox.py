#!/usr/bin/env python

# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Script for launching `python_toolbox` tests when installed in local Python.
'''


import test_python_toolbox


if __name__ == '__main__':
    test_python_toolbox.invoke_nose()