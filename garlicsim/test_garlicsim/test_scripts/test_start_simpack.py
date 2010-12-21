_help_text = '''\
This is a script for creating a skeleton for a `garlicsim` simpack. Use this
when you want to make a new simpack to have the basic folders and files created
for you.

    Usage: start_simpack.py my_simpack_name

The simpack will be created in the current path, in a directory with the name
of the simpack.
'''
        

def test_implicit_help():
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.execute(
                    argv=['start_simpack.py']
                )
            assert output_capturer.output == _help_text + '\n'
            assert glob.glob('*') == []
            
    finally:
        shutil.rmtree(temp_dir)
        

def test_explicit_help():
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.execute(
                    argv=['start_simpack.py', '--help']
                )
            assert output_capturer.output == _help_text + '\n'
            assert glob.glob('*') == []
            
    finally:
        shutil.rmtree(temp_dir)