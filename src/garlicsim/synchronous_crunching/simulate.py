import garlicsim
import history_browser

def simulate(simpack, state, iterations, *args, **kwargs):
    simpack_grokker = garlicsim.simpack_grokker.SimpackGrokker(simpack)
    if simpack_grokker.history_dependent:
        return __history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)
    else: # It's a non-history-dependent simpack
        return __non_history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)
        
    
    
def __history_simulate(simpack_grokker, state, iterations, *args, **kwargs):
    tree = garlicsim.state.tree()
    root = tree.add_state(state, parent=None)
    path = root.make_containing_path()
    history_browser = history_browser.HistoryBrowser(path)
    
    iterator = simpack_grokker.step_generator(history_browser, *args, **kwargs)
    
    for i in range(iterations-1):
        iterator.next()
        
    final_state = iterator.next()
    return final_state



def __non_history_simulate(simpack_grokker, state, iterations,
                           *args, **kwargs):
    
    iterator = simpack_grokker.step_generator(state, *args, **kwargs)
    for i in range(iterations-1):
        iterator.next()
        
    final_state = iterator.next()
    return final_state
