# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import abc

class HistoryBrowserABC(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_last_state(self):
        pass
    
    @abc.abstractmethod
    def __getitem__(self):
        pass
    
    @abc.abstractmethod
    def request_state_by_clock(self):
        pass
    
    @abc.abstractmethod
    def request_state_by_monotonic_function(self):
        pass
    
    @abc.abstractmethod
    def __len__(self):
        pass
    
    