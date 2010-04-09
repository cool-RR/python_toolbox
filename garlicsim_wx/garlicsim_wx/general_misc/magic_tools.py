import sys
import inspect
import re

def get_name_of_attribute_that_we_will_become():
    #clear_spaces = lambda s: ''.join(c for c in s if c != ' ')
    frame = sys._getframe().f_back.f_back.f_back
    module_name = frame.f_globals['__name__']
    line_number = frame.f_lineno - 1
    lines = inspect.getsourcelines(sys.modules[module_name])[0]
    match = None
    for line in lines[line_number::-1]:
        #clear_line = clear_spaces(line)
        match = re.search('self *\. *(.+?) *=', line)
        if match:
            break
    if match:
        name = match.group(1)
    else:
        name = None
    
    return name