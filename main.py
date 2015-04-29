#!/usr/bin/python
# coding=utf-8
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import time
import codecs
import sys
import cgi

from my_cgi.dispatcher import Dispatcher


reload(sys)
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()

PORT_NUMBER = 8888
RES_FILE_DIR = "."


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            # 根据请求的文件扩展名，设置正确的mime类型
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # 读取相应的静态资源文件，并发送它
                f = open(os.curdir + os.sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(u"没有找到响应请求")

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'
                     # 'CONTENT_TYPE': self.headers['Content-Type'],
            })
        print self.path
        keys = form.keys()
        params = ""
        for key in keys:
            params += key + "=" + form.getvalue(key, "") + "\n"
        print params[:len(params) - 1]

        if self.path.startswith("/cgi/"):
            print("dispatcher", self.path)
            dispatcher = Dispatcher(self.path, self, form)

        else:
            # 读取相应的静态资源文件，并发送它
            full_file_path = os.curdir + os.sep + self.path
            if os.path.isfile(full_file_path):
                file_out = open(full_file_path, 'rb')
                full_text = file_out.read()
                file_out.close()
                self.send_response(200)
                self.end_headers()
                if len(full_text) > 0:
                    self.wfile.write(full_text)
                    print(full_text)
                else:
                    self.wfile.write(u"{\"status\":1,\"remark\":\"请求处理不存在\"}")
            else:
                self.send_response(200)
                self.end_headers()
                retstr = u"{\"status\":-1,\"remark\":\"请求处理不存在,新建处理\"}"
                self.wfile.write(retstr)
                if not os.path.exists(os.path.split(full_file_path)[0]):
                    os.makedirs(os.path.split(full_file_path)[0])
                fwrite = codecs.open(full_file_path, 'wb', 'utf-8')
                fwrite.write(retstr)
                fwrite.close()
                print retstr, "已保存到文件，路径:", full_file_path


def get_data_string(self):
    now = time.time()
    clock_now = time.localtime(now)
    cur_time = list(clock_now)
    date_string = "%d-%d-%d-%d-%d-%d" % (cur_time[0],
                                         cur_time[1], cur_time[2], cur_time[3], cur_time[4], cur_time[5])
    return date_string


try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()