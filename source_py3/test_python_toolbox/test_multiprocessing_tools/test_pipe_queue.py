# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import multiprocessing

from python_toolbox import multiprocessing_tools

class Worker(multiprocessing.Process):
    def __init__(self, pipe_queue):
        self.pipe_queue = pipe_queue
        
    def run(self):
        connection = self.pipe_queue.wait_for_connection()
        message = connection.recv()
        assert message == 'Hello worker!'
        connection.send('Why hello there master!')
        message = connection.recv()
        assert message == 'Please exit mister worker!'
        

def test():
    pipe_queue = multiprocessing_tools.PipeQueue()
    workers = [Worker(pipe_queue) for _ in range(3)]
    