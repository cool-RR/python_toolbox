import time
import garlicsim
from garlicsim_wx.simulation_packages import life

if __name__ == '__main__':
    s = life.make_random_state()
    p = garlicsim.Project(life)
    n = p.root_this_state(s)
    p.crunching_manager.Cruncher = \
        garlicsim.asynchronous_crunching.crunchers.CruncherThread
    p.crunch_all_leaves(n, 100)
    p.sync_crunchers()
    time.sleep(10)
    p.sync_crunchers()
    