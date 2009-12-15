import enthought.mayavi.tools.mlab_scene_model
import multiprocessing

def f():
    return 7

if __name__ == '__main__':
    p = multiprocessing.Process(target=f)
    p.start()
    p.join()
