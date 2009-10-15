import time

import garlicsim
from garlicsim_wx.simulation_packages import life

if __name__ == "__main__":
        
    state = life.make_random_state()
    
    project = garlicsim.Project(life)
    
    node = project.root_this_state(state)
    
    project.maintain_buffer(node, 100)
    
    print(project.sync_crunchers())
    
    time.sleep(5)
    
    print(project.sync_crunchers())