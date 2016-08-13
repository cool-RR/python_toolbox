from python_toolbox import caching
from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing


@caching.cache()
def get_pseudo_random_strings(n):
    '''
    Get a list of random-like digit strings but ensure they're always the same.
    
    And also they're unique, i.e. no recurrences.
    '''
    some_pi_digits = str(math_tools.pi_decimal).split('.')[-1][:900]
    partitions = sequence_tools.partitions(some_pi_digits, partition_size=5)
    pseudo_random_numbers = nifty_collections.OrderedSet()
    for partition in partitions:
        if len(pseudo_random_numbers) == n:
            return tuple(pseudo_random_numbers)
        pseudo_random_numbers.add(partition)
    else:
        raise RuntimeError('Not enough unique pseudo-random numbers.')
    

