# coding=utf-8
__author__ = 'wangxiunian'
import json
import os


class Dispatcher:
    basePreStr = "/cgi/"
    responseHandler = None

    def __init__(self, path, handler, params):
        self.responseHandler = handler
        print path
        method = path[5:len(path)]
        if method == "listProject":
            keyWord = params.getvalue("keyWord", "")
            self.list_project(keyWord)
        else:
            resultMap = {'status': 0, 'remark': u"not find map"}
            handler.send_response(404)
            handler.send_header('Content-type', 'json/application')
            handler.end_headers()
            handler.wfile.write(json.dumps(resultMap))

    def return_data(self, data):
        self.responseHandler.send_response(200)
        self.responseHandler.send_header('Content-type', 'json/application')
        self.responseHandler.end_headers()
        if not data.has_key("status"):
            data["status"] = 1
            data["remark"] = "OK"
        self.responseHandler.wfile.write(json.dumps(data))
        return

    def list_project(self, keyWord):
        data = {"keyWord": keyWord}
        data["list"] = self.scan_files(os.curdir + os.sep, keyWord)
        self.return_data(data)

    def scan_files(self, directory, keyword):
        files_list = []

        for root, sub_dirs, files in os.walk(directory):
            for special_file in files:
                path = os.path.join(root, special_file)
                if keyword:
                    if keyword in path and (".git" not in path):
                        files_list.append(path)
                else:
                    if not self.check_folder_in([".git", ".js", ".idea", "my_cgi"], path):
                        files_list.append(os.path.join(root, special_file))
        return files_list

    def check_folder_in(self, excepts, path):
        for e in excepts:
            if e in path:
                return True
        return False