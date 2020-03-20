import os
from flask import Flask
from app import log_util as log

app = Flask(__name__)
app.config['RESOURCE_DIR'] = 'res'
app.config['DATA_DIR'] = 'res/images'
app.config['TEMP_DIR'] = 'res/tmp'
app.config['QUERY_DIR'] = 'queries'
from app import routes

log.init_logger(os.path.dirname(app.instance_path))
