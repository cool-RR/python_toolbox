# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.persistent.CrossProcessPersistent`.
'''

from __future__ import with_statement

import copy
import pickle
import cPickle

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import cute_testing

from garlicsim.general_misc import persistent
from garlicsim.general_misc.persistent import CrossProcessPersistent


class A(CrossProcessPersistent):
    pass    


def test():
    checkers = [_check_deepcopying]
    cross_process_persistents = [A(), CrossProcessPersistent()]
    
    iterator = cute_iter_tools.product(
        checkers,
        cross_process_persistents,
    )
    
    for checker, cross_process_persistent in iterator:
        yield checker, cross_process_persistent
    
        
def _check_deepcopying(cross_process_persistent):
    cross_process_persistent_deepcopy = copy.deepcopy(cross_process_persistent)
    assert cross_process_persistent_deepcopy is not cross_process_persistent
    
    cross_process_persistent_faux_deepcopy = copy.deepcopy(
        cross_process_persistent,
        persistent.DontCopyPersistent()
    )
    assert cross_process_persistent_faux_deepcopy is cross_process_persistent
    
    
def _check_process_passing(cross_process_persistent):
    pass

    
def test_helpful_warnings_for_old_protocols():
    pickle_modules = [pickle, cPickle]
    cross_process_persistents = [A(), CrossProcessPersistent()]
    old_protocols = [0, 1]
    
    iterator = cute_iter_tools.product(
        pickle_modules,
        cross_process_persistents,
        old_protocols
    )
    
    for pickle_module, cross_process_persistent, old_protocol in iterator:
        yield (_check_helpful_warnings_for_old_protocols, 
               pickle_module,
               cross_process_persistent,
               old_protocol)
            
    
def _check_helpful_warnings_for_old_protocols(pickle_module,
                                              cross_process_persistent,
                                              old_protocol):
    assert old_protocol < 2
    with cute_testing.RaiseAssertor(text=('protocol %s' % old_protocol)):
        pickle_module.dumps(cross_process_persistent,
                            protocol=old_protocol)