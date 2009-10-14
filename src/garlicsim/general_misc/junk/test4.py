import time
import garlicsim
from garlicsim_wx.simulation_packages import life


s = life.make_random_state(15, 15)
p = garlicsim.Project(life)
n = p.root_this_state(s)
p.crunch_all_leaves(n, 100)
for i in range(10):
    time.sleep(2)
    print(p.sync_crunchers())
    