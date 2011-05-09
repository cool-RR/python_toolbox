# blocktodo: delete this module

import os.path

from garlicsim.general_misc import temp_file_tools
from garlicsim.general_misc import sys_tools


def test_provoking_pypy():
    with temp_file_tools.TemporaryFolder() as temporary_folder:
        with sys_tools.TempSysPathAdder(temporary_folder):
            module_path = os.path.join(temporary_folder, 'module_meow.py')
            with open(module_path, 'w') as module_file:
                module_file.write('x = 5')
            import module_meow
            assert module_meow.x == 5
            

    assert module_meow.x == 5