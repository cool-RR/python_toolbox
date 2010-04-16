#tododoc

import types

import garlicsim_wx

class SimpackWxGrokker(object):
    '''

        
        tododoc: organize this:
        
        seek_bar_graphs = [live_cells, changes]
        
        # List of scalar state function and scalar history functions that should
        # be shown as graphs in the seek bar.
        
        ################################################
        
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
            raise Exception('''Simpack has no wx''') # todo: edit this
        
        self.__init_analysis_settings()
    
        
    
    def __init_analysis_settings(self):
        #tododoc
        
        # We want to access the `.settings` of our simpack_wx, but we don't know if
        # our simpack_wx is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        if isinstance(self.simpack_wx, types.ModuleType):
            try:
                __import__(''.join((self.simpack_wx.__name__, '.settings')))
                # This imports the `settings` submodule, but does *not* keep a
                # reference to it. We'll access it as an attribute of the
                # simpack below.
            
            except ImportError:
                pass
            
        
        original_settings = getattr(self.simpack_wx, 'settings', Settings())
            
        
        attribute_names = [
            'WORKSPACE_WIDGETS', 'SEEK_BAR_GRAPHS', 'STATE_VIEWER'
            ] # Should be defined somewhere else

        original_settings_dict = \
            dict(vars(original_settings)) if original_settings else {}
        

        fixed_settings_dict = {}
        for attribute_name in attribute_names:
            fixed_settings_dict[attribute_name] = \
                original_settings_dict.get(attribute_name, None)
            
        # todo: currently throws away unrecognized attributes from the simpack's
        # settings.
        
        self.settings = Settings()
        for (key, value) in fixed_settings_dict.iteritems():
            setattr(self.settings, key, value)
    