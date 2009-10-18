import time
import garlicsim
from garlicsim_wx.simulation_packages import life


s = life.make_random_state(15, 15)
p = garlicsim.Project(life)
n = p.root_this_state(s)
p.ensure_buffer(n, 100)
p.sync_crunchers()
time.sleep(10)
p.sync_crunchers()
    