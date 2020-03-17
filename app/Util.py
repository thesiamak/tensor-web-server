import sys
import os
import threading
import requests
import validators
from flask import request
from datetime import datetime

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/siamak/PycharmProjects/tensor3')
# noinspection PyUnresolvedReferences
import initiator
from .Object_detection_image import Detection


class BaseApi:
    data = {}
    status = False
    message = ""

    def get_result(self):
        return {'status': self.status, 'message': self.message, 'data': self.data}


class Query(BaseApi):
    target_file_path = ""

    def __init__(self):
        'download image to temp folder'
        url = request.args.get("img_url")
        if url is not None:
            validation = validators.url(url)
            if validation:
                stream = requests.get(url)
                dir_path = 'res/queries/' + datetime.today().strftime('%Y-%m-%d')
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                self.target_file_path = dir_path + "/" + datetime.today().strftime('%H_%M_%S_%f') + '.' + url.split('.')[
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

        return self.get_result()


class Train(BaseApi):

    def start(self):
        threading.Thread(target=initiator.run).start()
        self.status = True
        self.message = "training started ..."
        return self.get_result()


class Status(BaseApi):

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
        self.data["status"] = {"state": "idle", "total_queries": log_details[2], "total_trainings": log_details[1]}

        self.message = "Details generated successfully"
        self.status = True

        return self.get_result()

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
