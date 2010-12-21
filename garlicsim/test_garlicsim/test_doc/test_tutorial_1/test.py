# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for tutorial-1.'''

import re
import time

def test():
    '''Test tutorial-1.'''
    life_board_pattern = re.compile('^(([ #]{45}\n){24})([ #]{45})$')
    import garlicsim
    from garlicsim_lib.simpacks import life
    state = life.State.create_messy_root()
    assert life_board_pattern.match(repr(state))
    assert repr(type(state)) == \
        "<class 'garlicsim_lib.simpacks.life.state.State'>"
    new_state = garlicsim.simulate(state)
    assert life_board_pattern.match(repr(new_state))
    new_state = garlicsim.simulate(state, 20)
    assert life_board_pattern.match(repr(new_state))
    result = garlicsim.list_simulate(state, 20)
    assert repr(type(result)) == "<type 'list'>"
    assert len(result) == 21
    assert life_board_pattern.match(repr(result[0]))
    assert result[0] == state
    assert life_board_pattern.match(repr(result[-1]))
    assert life_board_pattern.match(repr(result[7]))
    repr(garlicsim.iter_simulate(state, 5)) # Not testing cause of pypy et al.
    assert (list(garlicsim.iter_simulate(state, 5)) == \
            garlicsim.list_simulate(state, 5))
    
    project = garlicsim.Project(life)
    state = life.State.create_diehard()
    assert life_board_pattern.match(repr(state))
    assert repr(state).count('#') == 7
    root = project.root_this_state(state)
    assert repr(root) == \
        ('<garlicsim.data_structures.Node with clock 0, '
         'root, leaf, touched, blockless, at %s>' % hex(id(root)))
    project.begin_crunching(root, 50)
    _result = project.sync_crunchers()
    assert repr(_result) == '<0 nodes were added to the tree>'
    (cruncher,) = project.crunching_manager.crunchers.values()
    while cruncher.is_alive():
        time.sleep(0.1)
    _result = project.sync_crunchers()
    assert repr(_result) == '<50 nodes were added to the tree>'
    assert repr(project.tree) == (
        '<garlicsim.data_structures.Tree with 1 roots, '
        '51 nodes and 1 possible paths at %s>' % hex(id(project.tree))
    )
    (path,) = project.tree.all_possible_paths()
    assert repr(path) == (
        '<garlicsim.data_structures.Path of length 51 '
        'at %s>' % hex(id(path))
    )    
    assert repr(path[-1]) == (
        '<garlicsim.data_structures.Node with clock 50, leaf, untouched, '
        'blockful, crunched with life.State.step_generator(<state>), at '
        '%s>' % hex(id(path[-1])))
    _state = path[-1].state
    assert repr(_state).count('#') == 24
    assert life_board_pattern.match(repr(_state))
    node = path[27]
    assert repr(node.state).count('#') == 20
    assert life_board_pattern.match(repr(node.state))
    new_node = project.fork_to_edit(node)
    new_node.state.board.set(28, 13, True)
    assert repr(new_node.state).count('#') == 21
    assert life_board_pattern.match(repr(new_node.state))
    new_node.finalize()
    assert repr(project.tree) == (
        '<garlicsim.data_structures.Tree with 1 roots, '
        '52 nodes and 2 possible paths at %s>' % hex(id(project.tree))
    )
    project.ensure_buffer(root, 50)
    _result = project.sync_crunchers()
    assert repr(_result) == '<0 nodes were added to the tree>'
    (cruncher,) = project.crunching_manager.crunchers.values()
    while cruncher.is_alive():
        time.sleep(0.1)
    _result = project.sync_crunchers()
    assert repr(_result) == '<23 nodes were added to the tree>'
    new_path = new_node.make_containing_path()
    assert repr(new_path[-1].state).count('#') == 49
    assert life_board_pattern.match(repr(new_path[-1].state))


