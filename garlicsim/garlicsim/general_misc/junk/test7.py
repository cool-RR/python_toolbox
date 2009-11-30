import garlicsim
from garlicsim.bundled.simulation_packages import queue

s = queue.make_plain_state()
l = garlicsim.list_simulate(queue, s, 100)
