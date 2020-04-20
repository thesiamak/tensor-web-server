import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class Config(object):
    DEBUG = True
    PROJECT_DIR = '/home/siamak/PycharmProjects/'
    RESOURCE_DIR = 'res'
    DATA_DIR = 'res/images'
    TEMP_DIR = 'res/tmp'
    QUERY_DIR = 'queries'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER = "http://" + get_ip() + ":8080"


class ProductionConfig(Config):
    DEBUG = False
