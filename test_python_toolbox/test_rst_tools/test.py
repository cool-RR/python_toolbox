from python_toolbox import rst_tools

def test():
    ''' '''
    html = rst_tools.rst_to_html("Title\n"
                                 "=====\n"
                                 "\n"
                                 "What's up doc?")
    assert "What's up doc?" in html