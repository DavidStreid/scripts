import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from shutil import copyfile

NUM_COLUMNS = 73
DESTINATION = './'

'''
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
files = {}

def getRowColumn(path):
    extension = '.txt'
    location = './'
    file = path.strip(extension).strip(location)
    attr = file.split('_')
    if(len(attr) != 3):
        raise ValueError('Could not parse %s' % path)
    row = int(attr[2])
    column = NUM_COLUMNS - int(attr[1])
    run = attr[0][-2:]
    return [row,column,run]

def copyFileToFolder(path,row,col,run):
    row = '0%d' % row if row < 10 else str(row)
    col = '0%d' % col if col < 10 else str(col)
    name = 'R%s_C%s_0000_00_%s.tif' % (row,col,run)
    dest = DESTINATION + name

    '''
    logic to make directories
    '''

    copyfile(path, dest)

class EventHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        try:
            path =  event.src_path
            [row,column,run] = getRowColumn(path)
            copyFileToFolder(path,row,column,run)
        except ValueError as err:
            print err
            return
    def on_moved(self, event):
        print ('File moved: %s' % event.src_path)
    def on_deleted(self, event):
        print ('File deleted: %s' % event.src_path)
    def on_modified(self, event):
        print ('File modified: %s' % event.src_path)

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