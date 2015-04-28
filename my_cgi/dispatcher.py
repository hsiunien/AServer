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
        data = {"keyword": keyWord}
        data["list"] = self.scan_files(os.curdir + os.sep, keyWord)
        self.return_data(data)

    def scan_files(self, directory, keyword):
        files_list = []
        for root, sub_dirs, files in os.walk(directory):
            for special_file in files:
                if keyword:
                    path = os.path.join(root, special_file)
                    if keyword in path:
                        files_list.append(path)
                else:
                    files_list.append(os.path.join(root, special_file))

        return files_list

