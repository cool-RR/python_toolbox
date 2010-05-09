# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Provides decorators to cache state- or history-dependent functions.

`state_cache` is for functions that take a state. `history_cache` is for
functions that take a history browser.
'''
#todo: make sure the cache gets lost on pickling
#todo: append to function's docstring?

from __future__ import with_statement

import weakref
import functools

import garlicsim

        

def state_cache(function):
    '''
    Caching decorator for state functions.
    
    This decorator should be used only on functions that have exactly one
    argument which is a state. (For example, in a Physics simulation you might
    want a function that takes a state and outputs the kinetic energy of that
    state.)
    
    On any subsequent calls to the function given the same state, the
    pre-calcluated value will be given from the cache instead of calculating it
    again.
    '''
    if hasattr(function, 'state_cache'): return function
    
    def cached(state):
        assert isinstance(state, garlicsim.data_structures.State)
        if state in cached.state_cache:
            return cached.state_cache[state]
        else:
            cached.state_cache[state] = value = function(state)
            return value
            
    cached.state_cache = weakref.WeakKeyDictionary()
    
    functools.update_wrapper(cached, function)
    
    return cached


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
                        end_node=node
                    )
            value = function(history_browser)
            cached.node_cache[node] = value
            return value
            
    cached.node_cache = weakref.WeakKeyDictionary()
    
    functools.update_wrapper(cached, function)
    
    return cached

if __name__ == '__main__': # make this into test
    import garlicsim
    from garlicsim_lib.simpacks import life

    s = life.make_random_state(10, 10)
    
    p = garlicsim.Project(life)
    
    r = p.root_this_state(s)
    
    p.simulate(r, 20)
    
    path = r.make_containing_path()
    
    @state_cache
    def live_cells(state):
        '''
        Meooww
        '''
        print('calculating for state %s' % id(state))
        return state.board._Board__list.count(True)
    
       
    for i in range(3):
        states = [node.state for node in path]
        print([live_cells(state) for state in states[-3:]])
    
    @history_cache
    def changes(history_browser):
        '''
        frrrr
        '''
        print('calculating for hb %s' % id(history_browser))
        try:
            state = history_browser[-1]
            last_state = history_browser[-2]
        except IndexError:
            return None
        
        board, last_board = state.board, last_state.board
        board_size = len(board._Board__list)
        counter = 0
        for i in xrange(board_size):
            if board._Board__list[i] != last_board._Board__list[i]:
                counter += 1
        return counter
    
    for i in range(3):
        print([changes(node) for node in path])
            
            
            
