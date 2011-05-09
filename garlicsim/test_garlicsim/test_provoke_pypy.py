# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for tutorial-2.'''

from __future__ import with_statement

import os.path

from garlicsim.general_misc.temp_value_setters import \
    TempWorkingDirectorySetter
from garlicsim.general_misc import sys_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import temp_file_tools

import garlicsim.scripts.start_simpack

#class Object(object):
    #pass

def test():
    '''Test provoking Pypy.'''
    
    import nose
    raise nose.SkipTest
    # Asserting we don't have a `_coin_flip` on path already in some other
    # place:
    assert not import_tools.exists('_coin_flip')
    
    with temp_file_tools.TemporaryFolder(prefix='test_garlicsim_') \
                                                          as temp_folder:
        with TempWorkingDirectorySetter(temp_folder):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.start(
                    argv=['start_simpack.py', '_coin_flip']
                )
            simpack_path = os.path.join(temp_folder, '_coin_flip')
                                                                      
            state_module_path = os.path.join(simpack_path, 'state.py')
                         
            with sys_tools.TempSysPathAdder(temp_folder):
                import _coin_flip                

                #o = Object()
                #o.simpack = _coin_flip
                simpack_grokker = garlicsim.misc.SimpackGrokker(_coin_flip)
                
                
            
            
    
        