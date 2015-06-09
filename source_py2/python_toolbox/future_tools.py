# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines tools related to the `concurrent.futures` standard library package.
'''

import time
import concurrent.futures

from python_toolbox import sequence_tools


class BaseCuteExecutor(concurrent.futures.Executor):
    '''
    An executor with extra functionality for `map` and `filter`.
    
    This is a subclass of `concurrent.futures.Executor`, which is a manager for
    parallelizing tasks. What this adds over `concurrent.futures.Executor`:

     - A `.filter` method, which operates like the builtin `filter` except it's
       parallelized with the executor.
     - An `as_completed` argument for both `.map` and `.filter`, which makes
       these methods return results according to the order in which they were
       computed, and not the order in which they were submitted.
     
    '''
    def filter(self, filter_function, iterable, timeout=None,
               as_completed=False):
        '''
        Get a parallelized version of `filter(filter_function, iterable)`.
        
        Specify `as_completed=False` to get the results that were calculated
        first to be returned first, instead of using the order of `iterable`.
        '''
        
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


    def map(self, function, iterable, timeout=None, as_completed=False):
        '''
        Get a parallelized version of `map(function, iterable)`.
        
        Specify `as_completed=False` to get the results that were calculated
        first to be returned first, instead of using the order of `iterable`.
        '''
        iterables = (iterable,)
        
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

    
class CuteThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor,
                             BaseCuteExecutor):
    '''
    A thread-pool executor with extra functionality for `map` and `filter`.
    
    This is a subclass of `concurrent.futures.ThreadPoolExecutor`, which is a
    manager for parallelizing tasks to a thread pool. What this adds over
    `concurrent.futures.ThreadPoolExecutor`:

     - A `.filter` method, which operates like the builtin `filter` except it's
       parallelized with the executor.
     - An `as_completed` argument for both `.map` and `.filter`, which makes
       these methods return results according to the order in which they were
       computed, and not the order in which they were submitted.
     
    '''    

class CuteProcessPoolExecutor(concurrent.futures.ProcessPoolExecutor,
                              BaseCuteExecutor):
    '''
    A process-pool executor with extra functionality for `map` and `filter`.
    
    This is a subclass of `concurrent.futures.ThreadPoolExecutor`, which is a
    manager for parallelizing tasks to a process pool. What this adds over
    `concurrent.futures.ThreadPoolExecutor`:

     - A `.filter` method, which operates like the builtin `filter` except it's
       parallelized with the executor.
     - An `as_completed` argument for both `.map` and `.filter`, which makes
       these methods return results according to the order in which they were
       computed, and not the order in which they were submitted.
     
    '''
