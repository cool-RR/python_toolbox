'''tododoc'''

import garlicsim.general_misc.third_party.decorator

@garlicsim.general_misc.third_party.decorator.decorator
def clear_redo_buffer(method, *args, **kwargs):
    self = args[0]
    del self.redo_buffer[:]
    return method(*args, **kwargs)


class EditingInterface(object):
    
    def __init__(self, gui_project):
        
        self.gui_project = gui_project
        
        self.undo_buffer = []
        
        self.redo_buffer = []
        
    def tree_delete_node_selection(self, node_selection):
        pass
    def undo(self):
        pass
    def redo(self):
        pass
        
        