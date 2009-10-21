import time
import garlicsim
from garlicsim.bundled.simulation_packages import life


state = life.make_random_state(40, 15)
print(state)
new_state = garlicsim.simulate(life, state)

p = garlicsim.Project(life)
n = p.root_this_state(state)
p.ensure_buffer(n, 100)
print(p.sync_crunchers())
time.sleep(10)
print(p.sync_crunchers())
    