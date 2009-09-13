import garlicsim
import history_browser as history_browser_module # Avoiding name clash

def path_simulate(simpack, state, iterations, *args, **kwargs):
    simpack_grokker = garlicsim.simpack_grokker.SimpackGrokker(simpack)
    if simpack_grokker.history_dependent:
        return __history_path_simulate(simpack_grokker, state, iterations,
                                       *args, **kwargs)
    else: # It's a non-history-dependent simpack
        return __non_history_path_simulate(simpack_grokker, state, iterations,
                                           *args, **kwargs)
        
    
    
def __history_path_simulate(simpack_grokker, state, iterations,
                            *args, **kwargs):
    tree = garlicsim.state.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser_module.HistoryBrowser(path)
    
    iterator = simpack_grokker.step_generator(history_browser, *args, **kwargs)
    
    current_node = root
    for i in range(iterations):
        current_state = iterator.next()
        current_node = tree.add_state(current_state, parent=current_node)
    
    return path



def __non_history_path_simulate(simpack_grokker, state, iterations,
                                *args, **kwargs):
    
    tree = garlicsim.state.Tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    
    iterator = simpack_grokker.step_generator(state, *args, **kwargs)
    
    current_node = root
    for i in range(iterations):
        current_state = iterator.next()
        current_node = tree.add_state(current_state, parent=current_node)
    
    return path
