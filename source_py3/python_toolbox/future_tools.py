# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import time
import concurrent.futures

from python_toolbox import sequence_tools


class CuteExecutorMixin:
    '''
    Coolness is filter and as_completed on both filter and map, blocktododoc
    '''
    def filter(self, filter_function, iterable, timeout=None,
               as_completed=False):
        '''Get a parallelized version of filter(filter_function, iterable).'''
        
        if timeout is not None:
            end_time = timeout + time.time()

        def make_future(item):
            future = self.submit(filter_function, item)
            future._item = item
            return future
            
        futures = tuple(map(make_future, iterable))
        futures_iterator = concurrent.futures.as_completed(futures) if \
                                                      as_completed else futures

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                for future in futures_iterator:
                    if timeout is None:
                        result = future.result()
                    else:
                        result = future.result(end_time - time.time())
                    if result:
                        yield future._item
            finally:
                for future in futures:
                    future.cancel()
        return result_iterator()


    def map(self, function, *iterables, timeout=None, as_completed=False):
        '''Get a parallelized version of map(function, iterable).'''
        
        if timeout is not None:
            end_time = timeout + time.time()

        futures = [self.submit(function, *args) for args in zip(*iterables)]
        futures_iterator = concurrent.futures.as_completed(futures) if \
                                                      as_completed else futures

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                for future in futures_iterator:
                    if timeout is None:
                        yield future.result()
                    else:
                        yield future.result(end_time - time.time())
            finally:
                for future in futures:
                    future.cancel()
        return result_iterator()

    
class CuteThreadPoolExecutor(CuteExecutorMixin,
                             concurrent.futures.ThreadPoolExecutor):
    pass

class CuteProcessPoolExecutor(CuteExecutorMixin,
                             concurrent.futures.ProcessPoolExecutor):
    pass
