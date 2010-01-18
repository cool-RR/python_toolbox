import os.path
import sys

try:
    import enthought
    import enthought.mayavi.tools.mlab_scene_model
finally:
    print(enthought.__file__)
    sys.stdout.flush()

import multiprocessing

def f():
    return 7

if __name__ == '__main__':
    p = multiprocessing.Process(target=f)
    p.start()
    p.join()
