# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing package for `python_toolbox`.'''

import sys
import pathlib

import pytest



def __bootstrap():
    '''
    Add needed packages in repo to path if we can't find them.

    This adds `python_toolbox`'s root folder to `sys.path` if it can't
    currently be imported.
    '''
    import os
    import sys
    import imp

    def exists(module_name):
        '''
        Return whether a module by the name `module_name` exists.

        This seems to be the best way to carefully import a module.

        Currently implemented for top-level packages only. (i.e. no dots.)

        Doesn't support modules imported from a zip file.
        '''
        assert '.' not in module_name
        try:
            imp.find_module(module_name)
        except ImportError:
            return False
        else:
            return True

    if not exists('python_toolbox'):
        python_toolbox_candidate_path = \
                                     pathlib(__file__).parent.parent.absolute()
        sys.path.append(python_toolbox_candidate_path)


__bootstrap()


def invoke_tests():
    '''Start Pytest using this `test_python_toolbox` test package.'''
    pytest.main()
    # nose.run(defaultTest='test_python_toolbox',
             # argv=(arguments + sys.argv[1:]))
