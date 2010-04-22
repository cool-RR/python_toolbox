import wx

class FlagRaiser(object): # todo: rename?
    def __init__(self, window, attribute_name=None,
                 value=True, function=None, delay=None):
        '''
        tododoc
        default for `function` is `window.Refresh`
        '''
        assert isinstance(window, wx.Window)
        self.window = window
        self.attribute_name = attribute_name
        self.value = value
        self.function = function or window.Refresh
        self.delay = delay
        if delay is not None:
            self._delay_in_ms = delay * 1000
            self.timer = wx.Timer()
            self.timer.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        
    def __call__(self):
        if self.attribute_name:
            setattr(self.window, self.attribute_name, self.value)
        if self.delay is None:
            self.function()
        else: # self.delay is a positive number
            if not self.timer.IsRunning():
                self.timer.Start(self._delay_in_ms, oneShot=True)
                
    def on_timer(self, event):
        self.function()