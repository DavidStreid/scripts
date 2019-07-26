from igo_transfer import transfer_to_igo_dir
from concurrent.futures import ThreadPoolExecutor
import os

TARGET_DIR = '%s/igoDir' % os.getcwd()
SRC_DIR = '%s/nikonDir' % os.getcwd()

def createFiles(dir):
    print('Creating files in %s' % dir)
    file = '%s/%s' % (dir,'X23c2_075_002.tif')
    open(file, 'a').close()
    print('\tFinished file creation')
    return

def test_created_dir(dir):
    # print('testing directory %s was created with correct files' % dir)
    for (root,dirs,files) in os.walk(dir, topdown=False):
        print(root)
        print(dirs)
        print(files)
        print('--------------------------------')
    return

executor = ThreadPoolExecutor(max_workers=2)
executor.submit(transfer_to_igo_dir, TARGET_DIR, SRC_DIR)
executor.submit(createFiles, SRC_DIR)
executor.submit(test_created_dir, TARGET_DIR)
