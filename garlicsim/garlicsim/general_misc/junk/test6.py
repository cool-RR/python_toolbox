import time
import garlicsim
from garlicsim.bundled.simulation_packages import life
from garlicsim.bundled.simulation_packages import prisoner

simpack = life

if __name__ == '__main__':
    
    state = simpack.make_random_state(10, 10)
    
    
    print(state)
    
    
    new_state = garlicsim.simulate(simpack, state, 10)
    
    print(new_state)
    
    result = garlicsim.list_simulate(simpack, state, 10)
    
    assert result[-1] == new_state
    
    print([thing.clock for thing in result])