import sys
import os
from shutil import copyfile
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from shutil import copyfile

# TODO - lint

NUM_COLUMNS = 73
DESTINATION = './'
SAMPLE = 'S0000'        # TODO - looks like this is set by the nikon macro
IGO_DIR_LOCATION = os.getcwd() # TODO - allow user to specify

'''
    igoDir - Tracks the structure of our IGO Directory. 

    {
        run: {
            sample: {
                column: {
                    row_column_sample_run.tif,...
                }
            }
        }

    }
'''
igo_dir = {}  

def get_row_column(path):
    extension = '.tif'      # TODO
    location = './'         # TODO
    file = path.strip(extension).strip(location)
    attr = file.split('_')
    if(len(attr) != 3):
        raise ValueError('Created file should have format [POS][RUN]_[COL]_[ROW]: %s' % path)
    row = int(attr[2])
    column = NUM_COLUMNS - int(attr[1])
    run = attr[0][-2:]
    return [row,column,run]

def put_directory_if_absent(dic, key, val, path, rsc):
    """
    Adds directory if absent in IGO directory. Returns state of directory mapped by key

    Args:
      dic (dict: str:dict/set): representation of directory
      key (str): file/directory name
      val (empty dict/set): Default value mapped by key if key doesn't exist
    """

    files = os.listdir(path)
    '''
    if key in dic:
        return dic[key]
    else:
    '''
    if key not in files:
        # TODO - make directory in correct location
        new_path = '%s/%s' % (path,rsc)
        os.mkdir(new_path)
        dic[key] = val
        return dic[key]
    else:
        print("IMPORTANT - %s was at path %s" % (key, path))

def copyFileToIgoDir(path,row,col,run):
    row = 'R' + ('0%d' % row if row < 10 else str(row))
    col = 'C' + ('0%d' % col if col < 10 else str(col))
    name = '%s_%s_0000_00_%s.tif' % (row,col,run)
    dest = DESTINATION + name

    dirPath = IGO_DIR_LOCATION
    runs = put_directory_if_absent(igo_dir, run, {},dirPath,run)
    dirPath = '%s/%s' % (IGO_DIR_LOCATION,run)
    samples = put_directory_if_absent(runs, SAMPLE, {},dirPath,SAMPLE)
    dirPath = '%s/%s' % (dirPath,SAMPLE)
    columns = put_directory_if_absent(samples, col, set(),dirPath,col)
    dirPath = '%s/%s' % (dirPath,col)

    # Check that name is not being added
    dirPath = '%s/%s' % (dirPath,name)
    copyfile(path,dirPath)
    columns.add(name)

    print(igo_dir)

class EventHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        try:
            path =  event.src_path
            [row,column,run] = get_row_column(path)
            copyFileToIgoDir(path,row,column,run)
        except ValueError as err:
            print(err)
            return
    def on_moved(self, event):
        print ('File moved - %s' % event.src_path)
    def on_deleted(self, event):
        print ('ERROR: File deleted - %s' % event.src_path)
    def on_modified(self, event):
        print ('File modified - %s' % event.src_path)

def getHandler():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = EventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    return my_event_handler

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = getHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
