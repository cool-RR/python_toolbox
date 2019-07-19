# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing package for `python_toolbox`.'''

import sys
import os
import pathlib
import importlib

import pytest



def __bootstrap():
    '''
    Add needed packages in repo to path if we can't find them.

    This adds `python_toolbox`'s root folder to `sys.path` if it can't
    currently be imported.
    '''
    if not importlib.util.find_spec('python_toolbox'):
        python_toolbox_candidate_path = \
                                     pathlib(__file__).parent.parent.absolute()
        sys.path.append(python_toolbox_candidate_path)


__bootstrap()


def invoke_tests():
    '''Start Pytest using this `test_python_toolbox` test package.'''
    os.chdir(os.path.dirname(__file__))
    pytest.main()
    # nose.run(defaultTest='test_python_toolbox',
             # argv=(arguments + sys.argv[1:]))
