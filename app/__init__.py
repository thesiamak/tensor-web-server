import os
from flask import Flask
from app import log_util as log
from app import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config.ProductionConfig())
db = SQLAlchemy(app)

from app.models import SpecieDb
from app import routes
log.init_logger(os.path.dirname(app.instance_path))
# db.drop_all()
db.create_all()
