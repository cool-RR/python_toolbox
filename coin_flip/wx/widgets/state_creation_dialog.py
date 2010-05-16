import wx
import garlicsim.data_structures


class StateCreationDialog(wx.Dialog):
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
    # should be the width and height of the new state.
    
    def __init__(self, frame):
        wx.Dialog.__init__(self, frame, title="Creating a root state")
        
        self.frame = frame

        # ...

        
    def start(self):
        # The `start` method will be used by `garlicsim_wx` after the dialog has
        # been created to make the dialog appear on the screen, and to create a
        # state object from the data that the dialog has collected from the
        # user. Returns a state, or None if the user hit "cancel" or something.
        if self.ShowModal() == wx.ID_OK:
            # state = ...
            pass
        else:
            state = None
        self.Destroy()
        return state
        


    
    