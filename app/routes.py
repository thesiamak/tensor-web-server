import os
from flask import request, url_for, send_from_directory, redirect
from app import app, Authentication, Util, Dictionary as Dic
from .log_util import logger


@app.errorhandler(404)
def own_404_page(error):
    return redirect(url_for('root'))


@app.route('/')
@logger
def root():
    if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
        return "You are in the root page of the Trainer app .\nYou might have been redirected(404 Error) here," \
               "so check the destination and entered URL ,and then try again please. "

    else:
        return Dic.Api.NOT_AUTHENTICATED


@app.route('/trainer/status')
@logger
def status():
    if Authentication.Auth(Authentication.ROLE.ADMIN).is_authenticated():
        return Util.Status().generate_status()

    else:
        return Dic.Api.NOT_AUTHENTICATED


@app.route('/trainer/train')
@logger
def train():
    if Authentication.Auth(Authentication.ROLE.ADMIN).is_authenticated():
        return Util.Train().start()

    else:
        return Dic.Api.NOT_AUTHENTICATED


@app.route('/trainer/query')
@logger
def query():
    if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
        return Util.Query().detect()

    else:
        return Dic.Api.NOT_AUTHENTICATED


@app.route('/trainer/download/<dir_name>/<filename>')
@logger
def download(dir_name, filename):
    if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
        if len(filename) > 4 and len(filename.split('.')) > 0 and len(dir_name) == 10:
            path = os.path.join(os.path.dirname(app.instance_path), app.config['RESOURCE_DIR'], app.config['QUERY_DIR'], dir_name)
            if os.path.isfile(path + '/' + filename):
                return send_from_directory(directory=path, filename=filename)
            else:
                return Dic.Api.NOT_FOUND_RESOURCE
        else:
            return Dic.Api.NOT_FOUND

    else:
        return Dic.Api.NOT_AUTHENTICATED


@app.route('/trainer/data', methods=["GET", "POST", "DELETE"])
@logger
def data():
    if request.method == "DELETE":
        if Authentication.Auth(Authentication.ROLE.ADMIN).is_authenticated():
            return Util.Data().delete()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    elif request.method == "POST":
        if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
            return Util.Data().post()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    elif request.method == "GET":
        if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
            return Util.Data().get()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    else:
        return Dic.Api.NOT_FOUND


@app.route('/plants', methods=["GET", "POST", "DELETE", "PUT"])
@logger
def plants():
    if request.method == "DELETE":
        if Authentication.Auth(Authentication.ROLE.ADMIN).is_authenticated():
            return Util.Specie().delete()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    elif request.method == "POST":
        if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
            return Util.Specie().add()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    elif request.method == "GET":
        if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
            return Util.Specie().get()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    elif request.method == "PUT":
        if Authentication.Auth(Authentication.ROLE.USER).is_authenticated():
            return Util.Specie().edit()
        else:
            return Dic.Api.NOT_AUTHENTICATED

    else:
        return Dic.Api.NOT_FOUND

