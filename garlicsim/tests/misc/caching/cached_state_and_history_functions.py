# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import copy
import nose

import garlicsim
from garlicsim_lib.simpacks import life
from garlicsim.misc import caching

def cached_state_function_test():
    
    def live_cells(state):
        live_cells.called_flag = True
        return state.board._Board__list.count(True)
    
    cached_live_cells = caching.state_cache(live_cells)
    
    s = life.State.create_root(5, 5)
    
    assert live_cells(s) == cached_live_cells(s) == cached_live_cells(s)
    
    live_cells.called_flag = False
    
    cached_live_cells(s)
    
    assert live_cells.called_flag is False
    
    
    l = garlicsim.list_simulate(s, 10)
    
    result_1 = [cached_live_cells(s) for s in l[0:5]]
        
    assert live_cells.called_flag is True
    live_cells.called_flag = False
    
    
    result_2 = [cached_live_cells(s) for s in l[0:5]]
    
    assert live_cells.called_flag is False
    
    assert result_1 == result_2
    
    
    result_1 = [cached_live_cells(s) for s in l]
        
    assert live_cells.called_flag is True
    live_cells.called_flag = False
    
    result_2 = [cached_live_cells(s) for s in l]
    
    assert live_cells.called_flag is False
    
    assert result_1 == result_2
    
    
    
def cached_history_function_test():
    
    @caching.history_cache
    def changes(history_browser):
        '''
        Return how many cells changed between the most recent state and its parent.
        '''
        changes.called_flag = True
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
    
    s = life.State.create_messy_root(5, 5)
    
    p = garlicsim.Project(life)
    
    r = p.root_this_state(s)
    
    leaf = p.simulate(r, 10)
    
    path = leaf.make_containing_path()
        
    result_1 = [changes(node) for node in list(path)[0:5]]
        
    assert changes.called_flag is True
    changes.called_flag = False
    
    
    result_2 = [changes(node) for node in list(path)[0:5]]
    
    assert changes.called_flag is False
    
    assert result_1 == result_2
    
    
    result_1 = [changes(node) for node in list(path)]
        
    assert changes.called_flag is True
    changes.called_flag = False
    
    
    result_2 = [changes(node) for node in list(path)]
    
    assert changes.called_flag is False
    
    assert result_1 == result_2
    

