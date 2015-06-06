# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import time
import concurrent.futures

from python_toolbox import sequence_tools


class CuteExecutorMixin:
    def filter(self, filter_function, iterable, timeout=None,
               as_completed=False):
        '''Get a parallelized version of filter(filter_function, iterable).'''
        
        sequence = sequence_tools.ensure_iterable_is_sequence(iterable)
        return (
            item for (item, keep) in zip(
                sequence,
                self.map(filter_function, sequence, timeout=timeout,
                         as_completed=as_completed)
            ) if keep
        )

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
                for future in futures:
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
