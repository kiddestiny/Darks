# -*- coding: utf-8 -*-
import sys
import time
import requests
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import idcard_recognize 



class CreatedEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(handler, event):
        print(event.src_path)
        file_name = event.src_path[2:]
        print('--'+file_name)
        if file_name.endswith('.jpeg'):
            print('jpeg match go...')
            res = idcard_recognize.process(event.src_path)
            print(res)
            s='http://127.0.0.1:8098/pushdata?address='+res['address']+'&gender='+res['sex']+'&user_name='+res['name']+''
            requests.get(s)
            print('end....')



if __name__ == "__main__":
    print('watch begin.....')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = '/Users/zhangmk/Desktop'
    event_handler = CreatedEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
