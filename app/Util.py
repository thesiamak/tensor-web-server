import sys
import cv2
import os
import threading
import requests
import validators
import urllib
import urllib3
from contextlib import closing
from zipfile import ZipFile
from shutil import copy2
from app import Dictionary as Dic
from app import app
from flask import request, send_from_directory
from datetime import datetime
from pathlib import Path
from app import SpecieDb
from app import db

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/siamak/PycharmProjects/tensor3')
# noinspection PyUnresolvedReferences
import initiator
from .Object_detection_image import Detection


class BaseApi:
    data = {}
    status = False
    message = ""

    def __init__(self) -> None:
        self.data = {}
        self.status = False
        self.message = ""

        super().__init__()

    def _get_result(self):
        return {'status': self.status, 'message': self.message, 'data': self.data}


class Query(BaseApi):
    target_file_path = ""

    def __init__(self):
        'download image to temp folder'
        super().__init__()
        url = request.args.get("img_url")
        if url is not None:
            validation = validators.url(url)
            if validation:
                stream = requests.get(url)
                dir_path = 'res/queries/' + datetime.today().strftime('%Y-%m-%d')
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                self.target_file_path = dir_path + "/" + datetime.today().strftime('%H_%M_%S_%f') + '.' + \
                                        url.split('.')[
                                            len(url.split('.')) - 1]
                tmp_file = open(self.target_file_path, 'wb')
                tmp_file.write(stream.content)
                tmp_file.close()

    def detect(self):
        if self.target_file_path == "":
            self.status = False
            self.message = "Invalid URL"

        else:
            self.status = True
            self.message = "Process has done detection"
            self.data = Detection(self.target_file_path, len(os.listdir('res/images'))).detect()

        return self._get_result()



class Train(BaseApi):

    def update(self):
        threading.Thread(target=initiator.start_inferencing).start()
        self.status = True
        self.message = "Graphs generation ordered ..."
        return self._get_result()


    def start(self):
        threading.Thread(target=initiator.run).start()
        self.status = True
        self.message = "training started ..."
        return self._get_result()


class Status(BaseApi):

    def _get_size(start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        size_in_MB = total_size / 1048576
        print(size_in_MB, 'size:')
        return str(total_size)

    def generate_status(self):

        'Generate a report around recent activities and status aof the system.'
        # get the list of data
        self.data["data"] = self.get_data_json()
        # get logs and cast them
        log_details = self.get_logs()
        self.data["logs"] = log_details[0]

        # total tests done so far
        # total trainings done
        # active state
        web_pack_size = "%s MB" % str(int(sum(
            f.stat().st_size for f in Path(os.path.join(app.config['PROJECT_DIR'], 'ODPyWS')).glob('**/*') if
            f.is_file()) / 1048576))

        temp_pack_size = "%s MB" % str(int(sum(
            f.stat().st_size for f in Path(os.path.join(app.config['PROJECT_DIR'], 'ODPyWS/res/tmp')).glob('**/*') if
            f.is_file()) / 1048576))

        detector_pack_size = "%s MB" % str(int(sum(
            f.stat().st_size for f in Path(os.path.join(app.config['PROJECT_DIR'], 'tensor3')).glob('**/*') if
            f.is_file()) / 1048576))

        self.data["status"] = {"state": "idle", "total_queries": log_details[2], "total_trainings": log_details[1],
                               'server_package_size': web_pack_size, 'detecotr_packege_size': detector_pack_size,
                               'temp_resource_size': temp_pack_size}

        self.message = "Details generated successfully"
        self.status = True

        return self._get_result()

    def get_data_json(self):
        dir_json = []
        for mDir in os.listdir(os.getcwd() + '/res/images/'):
            dir_json.append({'name': mDir, 'count': len(os.listdir(os.getcwd() + '/res/images/' + mDir))})
        return dir_json

    def get_logs(self):
        json = []

        for l_file in os.listdir(os.getcwd() + '/logs'):
            query_log_lines = []
            mlist = list(open(os.path.join(os.getcwd(), 'logs', l_file), "r"))
            index = 1
            while index < len(mlist):
                query_log_lines.append(mlist[len(mlist) - index])
                index += 1
            json.append({l_file.split(".")[0]: query_log_lines})

        training_log_lines = []
        tlist = list(open(os.getcwd() + '/../tensor3/logs/training_logs.txt', "r"))
        index = 1
        while index < len(tlist):
            training_log_lines.append(tlist[len(tlist) - index])
            index += 1
        json.append({'training_logs': training_log_lines})

        return json, len(
            list(self.find_all(training_log_lines.__str__(), '„„„„„„„„„„„„„„„„Done„„„„„„„„„„„„„„„„„„„„'))), len(
            list(self.find_all(query_log_lines.__str__(), "request query")))

    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub)  # use start += 1 to find overlapping matches


class Specie(BaseApi):

    def add(self):
        code = request.values.get("code")
        code_name = request.values.get("code_name")
        data = request.values.get("data")
        schema = request.values.get("schema")
        if SpecieDb.SpecieDb.query.filter_by(code=code).first():
            self.message = Dic.Api.DUPLICATE_RECORD
            self.status = False

        else:
            new_specie = SpecieDb.SpecieDb(code, code_name, data, schema)
            db.session.add(new_specie)
            db.session.commit()
            record = SpecieDb.SpecieDb.query.filter_by(code=code).first()
            self.data = record.serialize()
            self.message = Dic.Api.DONE
            self.status = True

        return self._get_result()

    def get(self):
        code = request.args.get("code")

        self.data["items"] = []
        if code:
            record = SpecieDb.SpecieDb.query.filter_by(code=code).first()
            if record:
                self.data = record.serialize()
                self.message = Dic.Api.DONE
                self.status = True
            else:
                self.message = Dic.Api.INVALID_INPUT
                self.status = False

        else:
            for item in SpecieDb.SpecieDb.query.all():
                self.data["items"].append(item.serialize())
                self.message = Dic.Api.DONE
                self.status = True

        return self._get_result()

    def delete(self):
        code = request.values.get("code")
        if code:
            record = SpecieDb.SpecieDb.query.filter_by(code=code).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                self.message = Dic.Api.DONE
                self.status = True

            else:
                self.message = Dic.Api.INVALID_INPUT
                self.status = False

        else:
            self.message = Dic.Api.INVALID_PARAM
            self.status = False

        return self._get_result()

    def edit(self):
        target_code = request.values.get("target_code")
        code = request.values.get("code")
        code_name = request.values.get("code_name")
        data = request.values.get("data")
        schema = request.values.get("schema")
        if target_code:
            record = SpecieDb.SpecieDb.query.filter_by(code=target_code).first()
            if record:
                record.update(code, code_name, data, schema)
                db.session.commit()
                self.message = Dic.Api.DONE
                self.status = True

            else:
                self.message = Dic.Api.INVALID_INPUT
                self.status = False

        else:
            self.message = Dic.Api.INVALID_PARAM
            self.status = False
        return self._get_result()


class Data(BaseApi):
    def get(self):
        code = request.args.get("code")
        if code is not None:

            target_dir = os.path.join(os.path.dirname(app.instance_path), app.config['DATA_DIR'], code)
            zip_file_path = os.path.join(os.path.dirname(app.instance_path), app.config['TEMP_DIR'])

            if os.path.isdir(target_dir):
                # with ZipFile(os.path.dirname(app.instance_path) + '/res/tmp/%s.zip' % code, 'w') as zipObj2:
                with ZipFile(app.config['TEMP_DIR'] + '/%s.zip' % code, 'w') as zipObj2:
                    for file in os.listdir(target_dir):
                        file = os.path.join(app.config['DATA_DIR'], code, file)
                        zipObj2.write(file)

                return send_from_directory(directory=zip_file_path, filename=code + '.zip')

            else:
                self.message = Dic.Api.NOT_FOUND_RESOURCE
                self.status = False
        else:
            self.message = Dic.Api.INVALID_PARAM
            self.status = False

        return self._get_result()

    def post(self):
        # download zip
        file_url = request.values.get('zip_url')
        item_id = request.values.get('id')

        if file_url is not None and item_id is not None:
            code_dir = os.path.join(app.config['DATA_DIR'], item_id)
            self.data['rejected_resources'] = []
            self.data['invalid_xml'] = []
            validation = validators.url(file_url)
            if validation:
                file_path = os.path.join(app.config['TEMP_DIR'], datetime.today().strftime('%H_%M_%S') + '.' + \
                                         file_url.split('.')[len(file_url.split('.')) - 1])

                self.download_file(file_url, file_path)

                # unzip
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(app.config["TEMP_DIR"]+"/" + item_id)

                # make dir in images

                if not os.path.isdir(code_dir):
                    os.mkdir(code_dir)
                for image in os.listdir(os.path.join(app.config['TEMP_DIR'], item_id)):
                    # check files and copy
                    if os.path.splitext(image)[1] == '.jpg':
                        height, width, channel = cv2.imread(os.path.join(app.config['TEMP_DIR'], item_id, image)).shape
                        if height > 300 and width > 300:
                            xml_file_path = os.path.join(app.config['TEMP_DIR'], item_id,
                                                         os.path.splitext(image)[0] + '.xml')
                            if os.path.isfile(xml_file_path):
                                copy2(os.path.join(app.config['TEMP_DIR'], item_id, image), code_dir)
                                copy2(xml_file_path, code_dir)
                                self.status = True
                                self.message = "Object added successfully"

                            else:
                                self.data['invalid_xml'].append(image)

                        else:
                            self.data['rejected_resources'].append(image)

            else:
                self.message = Dic.Api.INVALID_INPUT
                self.status = False
        else:
            self.message = Dic.Api.INVALID_PARAM
            self.status = False

        return self._get_result()

    def download_file(self, url, save_path):
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

    def delete(self):
        code = request.values.get('code')
        if code is not None:

            code_dir = os.path.join(app.config["DATA_DIR"], code)
            if os.path.isdir(code_dir):
                for file in os.listdir(code_dir):
                    os.remove(os.path.join(code_dir, file))

                os.removedirs(code_dir)
                self.message = 'Object %s removed.' % code
                self.status = True

            else:
                self.message = ' %s not found.'
                self.status = False
        else:
            self.message = Dic.Api.INVALID_PARAM
            self.status = False

        return self._get_result()
