#tododoc

import garlicsim

class SimpackGrokker(garlicsim.misc.SimpackGrokker):
    
    def __init__(self, simpack):
        garlicsim.misc.SimpackGrokker.__init__(self, simpack)
        self.__init_analysis_meta_wx()
        
    def __init_analysis_meta_wx(self):
        #tododoc
        
        attribute_names = ['workspace_widgets', 'seek_bar_graphs']

        original_meta_wx_dict = dict(vars(self.simpack.Meta_wx)) if \
                              hasattr(self.simpack, 'Meta_wx') else {}

        dict_for_fixed_meta_wx = {}
        for attribute_name in attribute_names:
            dict_for_fixed_meta_wx[attribute_name] = \
                original_meta_wx_dict.get(attribute_name, None)
            
        # todo: currently throws away unrecognized attributes from the simpack's
        # Meta_wx.
        
        self.Meta_wx = type('Meta_wx', (object,), dict_for_fixed_meta_wx)