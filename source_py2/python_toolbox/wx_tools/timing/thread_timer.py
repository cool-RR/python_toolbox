# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

# todo: daemonize?
# todo: kickass idea: make all timers use one thread that will sleep smartly
# to send all events correctly.

import threading
import time

import wx

from python_toolbox.wx_tools.timing import cute_base_timer


wxEVT_THREAD_TIMER = wx.NewEventType()
EVT_THREAD_TIMER = wx.PyEventBinder(wxEVT_THREAD_TIMER, 1)
'''Event saying that a `ThreadTimer` has fired.'''


class ThreadTimer(cute_base_timer.CuteBaseTimer):
    '''
    A timer for a wxPython app which runs on a different thread.

    This solved a problem of wxPython timers being late when the program is
    busy.
    '''

    n = 0
    '''The number of created thread timers.'''


    _EventHandlerGrokker__event_code = EVT_THREAD_TIMER


    def __init__(self, parent):
        '''
        Construct the ThreadTimer.

        `parent` is the parent window.
        '''

        cute_base_timer.CuteBaseTimer.__init__(self, parent)

        self.parent = parent
        '''The parent window.'''

        ThreadTimer.n += 1
        self.wx_id = wx.NewId()
        '''The ID of this timer, given by wxPython.'''

        self.__init_thread()
        self.alive = False
        '''Flag saying whether this timer is running.'''

    def __init_thread(self):
        '''Create the thread.'''
        thread_name = ''.join(('Thread used by ThreadTimer no. ', str(self.n)))
        self.thread = Thread(self, name=thread_name)
        # Overwriting previous thread, so it'll get garbage-collected,
        # hopefully

    def start(self, interval):
        '''Start the timer.'''
        if self.alive:
            self.stop()
        self.interval = interval
        self.alive = True
        self.thread.start()

    def stop(self):
        '''Stop the timer.'''
        self.alive = False
        self.thread.retired = True
        self.__init_thread()

    # Crutch for compatibilty with wx.Timer:
    Start = start
    Stop = stop

    def GetId(self):
        '''Get the wx ID of this timer.'''
        return self.wx_id


class Thread(threading.Thread):
    '''Thread used as a timer for wxPython programs.'''
    def __init__(self, parent, name):
        threading.Thread.__init__(self, name=name)
        self.parent = parent
        self.retired = False

    def run(self):
        '''Run the thread. Internal function.'''
        interval_in_seconds = self.parent.interval / 1000.0
        def sleep():
            time.sleep(interval_in_seconds)

        sleep()
        try:
            while self.parent.alive is True and self.retired is False:
                event = wx.PyEvent(self.parent.wx_id)
                event.SetEventType(wxEVT_THREAD_TIMER)
                wx.PostEvent(self.parent.parent, event)
                sleep()
        except:
            return # Just so it wouldn't raise an error when `wx` is shutting
                   # down
