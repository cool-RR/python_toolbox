import os.path
import sys

print(sys.path)
sys.stdout.flush()

try:
    import enthought.mayavi.tools.mlab_scene_model
finally:
    print(sys.path)
    sys.stdout.flush()

import multiprocessing

def f():
    return 7

if __name__ == '__main__':
    p = multiprocessing.Process(target=f)
    p.start()
    p.join()
