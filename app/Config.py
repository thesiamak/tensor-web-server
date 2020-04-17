import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    PROJECT_DIR = '/home/siamak/PycharmProjects/'
    RESOURCE_DIR = 'res'
    DATA_DIR = 'res/images'
    TEMP_DIR = 'res/tmp'
    QUERY_DIR = 'queries'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
