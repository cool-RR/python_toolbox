# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import time
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
    def get_n_alive_workers():
        return len([worker.alive() for worker in workers])
    def assert_n_live_workers(n):
        for i in range(5):
            if get_n_alive_workers() == n:
                return
            else:
                time.sleep(i)
        else:
            raise AssertionError
        
    connection_1 = pipe_queue.create_pipe()
    connection_1.send('Hello worker!')
    for worker in workers:
        worker.start()
    assert_n_live_workers(3)
    connection_2 = pipe_queue.create_pipe()
    connection_2.send('Hello worker!')
    message = connection_1.recv()
    assert message == 'Why hello there master!'
    message = connection_2.recv()
    assert message == 'Why hello there master!'
    assert_n_live_workers(3)
    connection_1.send('Please exit mister worker!')
    assert_n_live_workers(2)
    connection_2.send('Please exit mister worker!')
    connection_3 = pipe_queue.create_pipe()
    assert_n_live_workers(1)
    connection_3.send('Hello worker!')
    assert_n_live_workers(1)
    message = connection_3.recv()
    assert message == 'Why hello there master!'
    connection_3.send('Please exit mister worker!')
    assert_n_live_workers(1)
        
    
    