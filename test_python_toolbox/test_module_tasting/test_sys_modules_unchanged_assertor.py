# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing pacakge for `SysModulesUnchangedAssertor`.'''

from __future__ import with_statement

import sys
import uuid

import nose

from python_toolbox import cute_testing
from python_toolbox import module_tasting
from python_toolbox.module_tasting.sys_modules_unchanged_assertor \
                                            import SysModulesUnchangedAssertor

class MyException(Exception):
    pass
        
        
def test_without_change():
    '''
    Test that `SysModulesUnchangedAssertor` doesn't raise exception needlessly.
    '''
    with SysModulesUnchangedAssertor():
        pass


def test_with_change():
    '''Test `SysModulesUnchangedAssertor` raises exception when needed.'''    
    with SysModulesUnchangedAssertor():
        random_key = str(uuid.uuid4())
        with cute_testing.RaiseAssertor(exception_type=RuntimeError,
                                        text=' we expected `sys.modules` to '
                                             'be unchanged',
                                        assert_exact_type=True):
            with SysModulesUnchangedAssertor():
                sys.modules[uuid] = None
            
        assert uuid in sys.modules
        del sys.modules[uuid]
    

def test_error_propagation_without_change():
    '''
    Test that `SysModulesUnchangedAssertor` propagates any exception.
    
    This tests when `sys.modules` was not changed.
    '''
    with cute_testing.RaiseAssertor(exception_type=MyException,
                                    text='meow',
                                    assert_exact_type=True):        
        with SysModulesUnchangedAssertor():
            raise MyException('meow')
        

def test_error_propagation_with_change():
    '''
    Test that `SysModulesUnchangedAssertor` propagates any exception.
    
    This tests when `sys.modules` was changed.
    '''
    with SysModulesUnchangedAssertor():
        random_key = str(uuid.uuid4())
        with cute_testing.RaiseAssertor(exception_type=MyException,
                                        text='frrr',
                                        assert_exact_type=True):        
            with SysModulesUnchangedAssertor():
                sys.modules[uuid] = None
                raise MyException('frrr')
            
        
        assert uuid in sys.modules
        del sys.modules[uuid]
    
