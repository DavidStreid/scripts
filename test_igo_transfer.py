from igo_transfer import transfer_to_igo_dir, extract_well_index, get_row_column
from concurrent.futures import ThreadPoolExecutor
import random
import os
import sys
import unittest
import shutil
import subprocess
import time

class TestStringMethods(unittest.TestCase):
    def setup_nikon_igo(self, nikon, igo):
        if not os.path.exists(igo):
            print('Creating igo dir at %s' % igo)
            os.mkdir(igo)
        if not os.path.exists(nikon):
            print('Creating nikon dir at %s' % nikon)
            os.mkdir(nikon)
        return 'Finished setup`'

    def create_files(self,dir):
        print('Creating mock nikon files')
        try:
            for char_code in range(65,89):  # 'A': 65, 'Z': 88
                row_idx = chr(char_code)
                for col_idx in range(1,25):
                    for run in ['c1','c2']:
                        for row in range(1,4):
                            for col in range(1,4):
                                file_name = '%s/%s%02d%s_00%d_00%d.tif' % (dir,row_idx,col_idx,run,col,row)
                                f = open(file_name, 'w')
                                f.write(file_name)
                                f.close()
        except Exception as err:
            print(err)
        return 'Finished mock file creation'

    def verify_file_contents(self, dir):
        print('Verifying file contents of dir: %s' % dir)
        test_dic = {
            'R01_C01_0000_00_c1.tif': 'A01c1_001_001.tif',
            'R04_C04_0000_00_c1.tif': 'B02c1_001_001.tif',
            'R70_C70_0000_00_c1.tif': 'X24c1_001_001.tif',
            'R71_C41_0000_00_c2.tif': 'X14c2_002_002.tif',
        }
        try:
            for root, dirs, files in os.walk(dir):
                for name in files:
                    if name in test_dic:
                        print(name)
                        f=open(os.path.join(root, name), "r")
                        contents=f.read()
                        contents_path = contents.split('/')
                        f.close()
                        self.assertEqual(contents_path[-1],test_dic[name])
        except Exception as err:
            print(err)
        return 'Finished verifying file contents'

    def test_igo_directory_creation(self):
        TARGET_DIR = '%s/igoDir' % os.getcwd()
        SRC_DIR = '%s/nikonDir' % os.getcwd()

        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                print(executor.submit(self.setup_nikon_igo, TARGET_DIR, SRC_DIR).result())
                f1 = executor.submit(transfer_to_igo_dir, TARGET_DIR, SRC_DIR)
                print(executor.submit(self.create_files, SRC_DIR).result())
                print(executor.submit(self.verify_file_contents, TARGET_DIR).result())
        except Exception as err:
            print(err)
        """
        print('testing directory %s was created with correct files' % TARGET_DIR)
        for (root,dirs,files) in os.walk(TARGET_DIR, topdown=False):
            print(root)
            print(dirs)
            print(files)
            print('--------------------------------')
        return
        """

    def test_extract_well_index(self):
        [col_idx,row_idx] = extract_well_index('A01')
        self.assertEqual(row_idx, 0)
        self.assertEqual(col_idx, 0)

        [col_idx,row_idx] = extract_well_index('B03')
        self.assertEqual(row_idx, 1)
        self.assertEqual(col_idx, 2)

    def test_get_row_column(self):
        [row,col,run] = get_row_column('A15c2_002_003.tif')
        self.assertEqual(row,3)
        self.assertEqual(col,44)
        self.assertEqual(run,'c2')

        [row,col,run] = get_row_column('Z22c1_003_001.tif')
        self.assertEqual(row,76)
        self.assertEqual(col,66)
        self.assertEqual(run,'c1')

if __name__ == '__main__':
    unittest.main()


