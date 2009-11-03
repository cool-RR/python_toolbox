import psyco
psyco.full()

from garlicsim.general_misc.logic_tools import all_equal

stuff = [[1, 'meow'] for i in range(10)]

print all_equal(stuff)