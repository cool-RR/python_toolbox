#tododoc

import types

import garlicsim_wx

class Settings(object):
    #todo: subclass from a pretty vars-shower
    def __init__(self):
        self.BIG_WORKSPACE_WIDGETS = []
        self.SMALL_WORKSPACE_WIDGETS = []
        self.SEEK_BAR_GRAPHS = []
        '''
        List of scalar state function and scalar history functions that should
        be shown as graphs in the seek bar.
        '''
        self.STATE_CREATION_DIALOG = garlicsim_wx.misc.StateCreationDialog

class SimpackWxGrokker(object):
    '''

        
        
    '''
    def __init__(self, simpack):
        self.simpack = simpack
        
        if isinstance(simpack, types.ModuleType):
            try:
                __import__(''.join((simpack.__name__, '.wx')))
            except ImportError:
                pass
        try:
            self.simpack_wx = self.simpack.wx
        except AttributeError:
            self.simpack_wx = None
            #raise Exception('''Simpack has no wx''') # todo: edit this
        
        self.__init_analysis_settings()
    
        
    
    def __init_analysis_settings(self):
        #tododoc
        
        # We want to access the `.settings` of our simpack_wx, but we don't know if
        # our simpack_wx is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        self.settings = Settings()        
        
        if isinstance(self.simpack_wx, types.ModuleType):
            try:
                __import__(''.join((self.simpack_wx.__name__, '.settings')))
                # This imports the `settings` submodule, but does *not* keep a
                # reference to it. We'll access it as an attribute of the
                # simpack below.
            
            except ImportError:
                pass
            
        # Checking if there are original settings at all. If there aren't, we're
        # done.
        if self.simpack_wx and hasattr(self.simpack_wx, 'settings'):
            
            original_settings = getattr(self.simpack_wx, 'settings')
        
            for (key, value) in vars(self.settings).iteritems():
                if hasattr(original_settings, key):
                    actual_value = getattr(original_settings, key)
                    setattr(self.settings, key, actual_value)
            # todo: currently throws away unrecognized attributes from the
            # simpack's settings.
                
    