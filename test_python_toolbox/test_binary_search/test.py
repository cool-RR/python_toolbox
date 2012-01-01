from python_toolbox import binary_search
from python_toolbox import nifty_collections
from python_toolbox import misc_tools


def test():
    ''' '''
    my_list = [0, 1, 2, 3, 4]
    
    assert binary_search.binary_search(
        my_list,
        misc_tools.identity_function,
        3,
        binary_search.EXACT
    ) == 3
    
    assert binary_search.binary_search(
        my_list,
        misc_tools.identity_function,
        3.2,
        binary_search.CLOSEST
    ) == 3
    
    assert binary_search.binary_search(
        my_list,
        misc_tools.identity_function,
        3.2,
        binary_search.BOTH
    ) == (3, 4)