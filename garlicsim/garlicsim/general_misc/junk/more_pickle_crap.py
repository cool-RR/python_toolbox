from garlicsim.general_misc import pickle_tools
pickle_module = pickle_tools.pickle_module


import multiprocessing, threading

l = threading.RLock() #l = multiprocessing.RLock()

#pickle_tools.is_atomically_pickleable(l)

pickle_module.dumps(l)