import garlicsim.simpack_grokker

def simulate(simpack, state, iterations, *args, **kwargs):
    simpack_grokker = garlicsim.simpack_grokker.SimpackGrokker(simpack)
    if simpack_grokker.history_dependent:
        return __history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)
    else: # It's a non-history-dependent simpack
        return __non_history_simulate(simpack_grokker, state, iterations,
                                  *args, **kwargs)
        
def __history_simulate(simpack_grokker, state, iterations, *args, **kwargs):
    
    pass


def __non_history_simulate(simpack_grokker, state, iterations, *args, **kwargs):
    iterator = simpack_grokker.step_generator(state, *args, **kwargs)
    for i in range(iterations-1):
        iterator.next()
        
    final_state = iterator.next()
    return final_state
