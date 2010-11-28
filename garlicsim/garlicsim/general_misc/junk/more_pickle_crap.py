from garlicsim.general_misc import pickle_tools
pickle_module = pickle_tools.pickle_module


import cStringIO

i = cStringIO.StringIO()

pickle_module.dumps(i)

0