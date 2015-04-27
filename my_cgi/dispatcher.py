# coding=utf-8
__author__ = 'wangxiunian'
import json
import os


class Dispatcher:
    def __init__(self, path, handler):
        print path
        resultMap = {'status': 1, 'remark': "可以"}
        handler.send_response(200)
        handler.send_header('Content-type', 'json/application')
        handler.end_headers()
        handler.wfile.write(json.dumps(resultMap))


def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list


print(os.curdir + os.sep)