# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `history_cache` decorator.

See its documentation for more information.
'''

# todo perhaps reorganize
#todo: make sure the cache gets lost on pickling

from __future__ import with_statement

import weakref
import functools

import garlicsim


def history_cache(function, *args, **kwargs):
    '''
    Caching decorator for functions that take a history browser.
    
    This decorator should be used only on functions that have exactly one
    argument which is a history browser. (For example, in a cellular automata
    simulation you might want a function that takes a history browser and tells
    you how many cells changed value between the most recent state and the one
    before it.)
    
    Note that the raw function will take a history browser, but the decorated
    function will take a node, for which a history browser will be created and
    fed into the original function.
    
    On any subsequent calls to the function given the same node, the
    pre-calcluated value will be given from the cache instead of calculating it
    again.
    '''
    if hasattr(function, 'node_cache'):
        return function
    
    def cached(node):
        assert isinstance(node, garlicsim.data_structures.Node)
        if node in cached.node_cache:
            return cached.node_cache[node]
        else:
            path = node.make_containing_path()
            with node.tree.lock.read:
                history_browser = \
                    garlicsim.synchronous_crunching.HistoryBrowser(
                        path=path,
                        tail_node=node
                    )
            value = function(history_browser)
            cached.node_cache[node] = value
            return value
            
    cached.node_cache = weakref.WeakKeyDictionary()
    
    functools.update_wrapper(cached, function)
    cached.__wrapped__ = function
    
    return cached
