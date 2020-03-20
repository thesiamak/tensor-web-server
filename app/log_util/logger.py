#! /usr/bin/python
from datetime import datetime
import os


class Logger:
    _recorder_file_pointer = ""
    _file_path = 'logs/'

    def __init__(self, base_path, target='system'):
        self._file_path = os.path.join(base_path, self._file_path, target + '.txt')

    def _open_file(self):
        try:
            if os.path.isfile(self._file_path):
                self._recorder_file_pointer = open(self._file_path, 'a+')
            else:
                self._recorder_file_pointer = open(self._file_path, 'w+')

        except FileNotFoundError:
            print("Log File not accessible in : " + self._file_path)
            self._close_file()

    def _close_file(self):
        self._recorder_file_pointer.close()

    def record(self, event):
        self._open_file()
        event = "%s | Logger: %s\n" % (datetime.today().strftime('%Y/%m/%d %H:%M:%S'), event)
        self._recorder_file_pointer.write(event)
        self._close_file()


