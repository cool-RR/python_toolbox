# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `set_process_priority` function.

See its documentation for more info.
'''

def set_process_priority(priority, pid=None):
    '''
    Set the priority of a Windows process.

    Priority is a value between 0-5 where 2 is normal priority. Default sets
    the priority of the current Python process but can take any valid process
    ID.
    '''

    import win32process, win32con, win32api

    priorityclasses = [
        win32process.IDLE_PRIORITY_CLASS,
        win32process.BELOW_NORMAL_PRIORITY_CLASS,
        win32process.NORMAL_PRIORITY_CLASS,
        win32process.ABOVE_NORMAL_PRIORITY_CLASS,
        win32process.HIGH_PRIORITY_CLASS,
        win32process.REALTIME_PRIORITY_CLASS
    ]

    if pid is None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])