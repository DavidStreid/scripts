import sys
import os
from shutil import copyfile
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from shutil import copyfile

# TODO - lint

IGO_DIR_LOCATION = '.'
SAMPLE = 'S0000'        # TODO - looks like this is set by the nikon macro

def extract_well_index(well):
    """
    Extracts the upper-right (row, column) position of a 3x3 well on the plate

    Args:
      well (str): Well ('X##', 'X' indicates set of 3-rows and '##' indicates the set of 3-columns. e.g. 'A01')
    """
    if len(well) != 3:
        print('Well should be of format X##, e.g. \'AO1\': %s' % well)
    if not well[0].isalpha():
        print('First character of well should be a letter: %s' % well)
    if not well[1:].isdigit():
        print('Last characters of well should be digits: %s' % well)

    well_char = well[0].lower() # a: 97, z: 122
    # TODO - Verify
    well_pos = int(well[1:])
    row_idx = ord(well_char) - 97
    col_idx = well_pos-1
    return [col_idx, row_idx]

def get_row_column(path):
    extension = '.tif'      # TODO
    location = './'         # TODO
    file = path.strip(extension).strip(location)
    attr = file.split('_')
    if(len(attr) != 3):
        raise ValueError('Created file should have format [POS][RUN]_[COL]_[ROW]: %s' % path)

    well = attr[0][-5:-2]
    [col_idx, row_idx] = extract_well_index(well)
    rel_row = int(attr[2])
    rel_col = int(attr[1])

    # Wells are 3x3
    row = (row_idx*3) + rel_row
    col = (col_idx*3) + rel_col

    # TODO - validation check on row & column
    run = attr[0][-2:]        # c1/c2
    return [row,col,run]

def put_directory_if_absent(path, rsc):
    """
    Adds directory if absent in destination directory

    Args:
      path (str): target directory
      rsc (str): resource to be written to target directory
    """
    files = os.listdir(path)
    next_path = '%s/%s' % (path,rsc)
    if rsc not in files:
        os.mkdir(next_path)
    else:
        print("IMPORTANT - %s was at path %s" % (rsc, path))
    return next_path

def copyFileToIgoDir(path,dest,row,col,run):
    row = 'R' + ('0%d' % row if row < 10 else str(row))
    col = 'C' + ('0%d' % col if col < 10 else str(col))
    name = '%s_%s_0000_00_%s.tif' % (row,col,run)

    dir_path = dest
    dir_path = put_directory_if_absent(dir_path,run)
    dir_path = put_directory_if_absent(dir_path,SAMPLE)
    dir_path = put_directory_if_absent(dir_path,col)

    file_path = '%s/%s' % (dir_path,name)
    # TODO - Check that name is not being added
    copyfile(path,file_path)

class EventHandler(PatternMatchingEventHandler):
    def __init__(self, dest, patterns, ignore_patterns, ignore_directories, case_sensitive):
       PatternMatchingEventHandler.__init__(self,patterns, ignore_patterns, ignore_directories, case_sensitive)
       self.dest = dest
    def on_created(self, event):
        try:
            path =  event.src_path
            [row,column,run] = get_row_column(path)
            copyFileToIgoDir(path,self.dest,row,column,run)
        except ValueError as err:
            print(err)
            return
        except Exception as err:
            print(err)
            return
    def on_moved(self, event):
        print ('File moved - %s' % event.src_path)
    def on_deleted(self, event):
        print ('ERROR: File deleted - %s' % event.src_path)
    def on_modified(self, event):
        print ('File modified - %s' % event.src_path)

def getHandler(dest):
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = EventHandler(dest,patterns, ignore_patterns, ignore_directories, case_sensitive)
    return my_event_handler

def transfer_to_igo_dir(dest = '.', src = '.'):
    print('Writing files from %s to %s' % (src, dest))
    event_handler = getHandler(dest)
    observer = Observer()
    observer.schedule(event_handler, src, recursive=True)
    observer.start()
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    TARGET_DIR = '%s/igoDir' % os.getcwd()
    SRC_DIR = '%s/nikonDir' % os.getcwd()
    transfer_to_igo_dir(TARGET_DIR, SRC_DIR)