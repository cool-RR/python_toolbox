from python_toolbox.path_tools import get_root_path_of_module

def test():
    ''' '''
    import email.charset
    import re
    assert get_root_path_of_module(email) == \
           get_root_path_of_module(email.charset) == \
           get_root_path_of_module(re) 