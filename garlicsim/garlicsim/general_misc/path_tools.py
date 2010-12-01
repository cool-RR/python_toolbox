import os.path
import glob


def list_sub_folders(path):
    assert os.path.isdir(path)
    files_and_folders = glob.glob(os.path.join(path, '*'))
    folders = filter(os.path.isdir, files_and_folders)
    return folders