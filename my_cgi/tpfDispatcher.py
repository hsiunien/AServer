# coding=utf-8
__author__ = 'wangxiunian'
import os
import codecs


class TpfDispatcher:
    responseHandler = None

    def __init__(self, handler, path):
        self.responseHandler = handler
        self.return_data(path)


    def return_data(self, path):
        # 读取相应的静态资源文件，并发送它
        full_file_path = os.curdir + os.sep + path
        if os.path.isfile(full_file_path):
            file_out = open(full_file_path, 'rb')
            full_text = file_out.read()
            file_out.close()
            self.responseHandler.send_response(200)
            self.responseHandler.end_headers()
            if len(full_text) > 0:
                self.responseHandler.wfile.write(full_text)
                print(full_text)
            else:
                self.responseHandler.wfile.write(u"{\"status\":1,\"remark\":\"请求处理不存在\"}")
        else:
            self.responseHandler.send_response(200)
            self.responseHandler.end_headers()
            retstr = u"{\"resultCode\":-1,\"errorDesc\":\"请求处理不存在,新建处理\"}"
            self.responseHandler.wfile.write(retstr)
            if not os.path.exists(os.path.split(full_file_path)[0]):
                os.makedirs(os.path.split(full_file_path)[0])
            fwrite = codecs.open(full_file_path, 'wb', 'utf-8')
            fwrite.write(retstr)
            fwrite.close()
            print retstr, "已保存到文件，路径:", full_file_path


print(os.path.curdir + os.sep + ".js" + os.sep)