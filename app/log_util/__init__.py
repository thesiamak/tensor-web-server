from flask import request, jsonify

from functools import wraps
from .EVENT import EVENT, Target
from .logger import Logger
import glob
import os
import shutil

_loggers = {}
_base_path = ''


def init_logger(base_path):
    global _base_path
    _base_path = base_path


def logger(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        message = "%s - %s - %s " % (dict(request.args), dict(args),  dict(kwargs))
        log("API_" + function.__name__, message)
        return function(*args, **kwargs)
    return wrapper


def log(target, event):
    global _loggers
    try:
        _loggers[target].record(event)

    except KeyError:
        _loggers[target] = Logger(_base_path, target)
        log(target, event)


def remove_files(path):
    files = glob.glob(path + '/*.*', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def clear_dir(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
