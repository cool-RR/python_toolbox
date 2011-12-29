import wx
import garlicsim.data_structures
from garlicsim_wx.widgets.misc import BaseStateCreationDialog


class StateCreationDialog(BaseStateCreationDialog):
    # This is where you define a dialog for creating a root state.
    #
    # When someone loads your simpack into `garlicsim_wx` and starts a new
    # simulation, the first thing he sees is the state creation dialog. The
    # state creation dialog is a convenient way to create the first state in
    # your program.
    #
    # This dialog should display some kind of form for the user to fill out.
    # This will usually ask the user question about how they want their initial
    # state to be. For example, for a Life simpack the dialog will ask what
    # the width and height of the new state should be.
    
    def __init__(self, frame):
        BaseStateCreationDialog.__init__(self,
                                         frame,
                                         title='Creating a root state')
        
        self.frame = frame

        # Store the state that you create as the `.state` attribute:
        self.state = None
        # When the dialog is finished, GarlicSim will take the new state from
        # this attribute. (Assuming the user clicked "Ok" and not "Cancel".)

        
        # ... Build your widgets/sizers/event-bindings here!


    
    