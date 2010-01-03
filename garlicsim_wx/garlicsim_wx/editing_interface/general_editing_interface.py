'''tododoc'''


from base_editing_interface import BaseEditingInterface


class GeneralEditingInterface(BaseEditingInterface):
    
    def __init__(self, gui_project):
        
        self.gui_project = gui_project
        
    def undo(self):
        
        
        