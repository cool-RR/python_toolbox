import garlicsim
from garlicsim_lib.simpacks import queue

s = queue.make_plain_state()
l = garlicsim.list_simulate(queue, s, 100)
