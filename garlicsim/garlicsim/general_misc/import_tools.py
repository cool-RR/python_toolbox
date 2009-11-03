'''tododoc'''

import os.path
import imp
from garlicsim.general_misc import package_finder

def import_all(path):
    
    paths = package_finder(path)
    
    names = {}
    for path in paths:
        names[path] = os.path.splitext(os.path.split(path)[1])[0]
    
    d = {}
    
    for (path, name) in names:
        d[name] = import_by_path(path)
    
    return d
        
    
    
        
    
    
    

