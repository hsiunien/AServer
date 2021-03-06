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
import urlparse
from json import JSONDecoder

from my_cgi.dispatcher import Dispatcher
from my_cgi.cashbox_api_dispatcher import CashboxApiDispatcher
from my_cgi.tpfDispatcher import TpfDispatcher


reload(sys)
sys.setdefaultencoding("utf-8")
print sys.getdefaultencoding()

PORT_NUMBER = 9001
RES_FILE_DIR = "."


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            # 根据请求的文件扩展名，设置正确的mime类型
            parsed_path = urlparse.urlparse(self.path)
            tp = parsed_path.query

            print(tp)
            self.path = self.path.split("?")[0]
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".xml"):
                mimetype = 'text/xml'
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
            if self.path.endswith(".json"):
                mimetype = 'application/json'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True
            if sendReply == True:
                # 读取相应的静态资源文件，并发送它
                f = open(os.curdir + os.sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', "application")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                exist = os.path.exists(os.curdir + os.sep + self.path)
                if exist:
                    f = open(os.curdir + os.sep + self.path, 'rb')
                    mimetype = 'application/octet-stream'
                    self.send_response(200)
                    self.send_header('Content-type', "application")
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(u"没有找到响应请求")

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        print self.path
        print self.headers
        if self.headers.getheader('content-type') is not None:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if self.path.endswith("gateway.htm") and (ctype == 'text/plain' or ctype == "application/json"):
            length = int(self.headers.getheader('content-length'))
            postStr = self.rfile.read(length)
            print(postStr)
            dict = JSONDecoder().decode(postStr)
            dispatcher = CashboxApiDispatcher(dict["serviceId"], dict["requestBody"], self, dict)
        else:
            # 打印请求参数
            if ctype == 'text/plain' or ctype == "application/json":
                length = int(self.headers.getheader('content-length'))
                postStr = self.rfile.read(length)
                print(postStr)
            else:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'
                             # 'CONTENT_TYPE': self.headers['Content-Type'],
                    })
                params = ""
                if form.list is not None:
                    keys = form.keys()
                    for key in keys:
                        if key == "image":
                            fwrite = codecs.open(os.curdir + os.sep + key + ".jpg", 'wb')
                            fwrite.write(form.getvalue(key, "none"))
                            fwrite.close()
                            print("found file" + key)
                        elif key == "images":
                            list = form.getlist(key);
                            for img in list:
                                fwrite = codecs.open(os.curdir + os.sep + key + ".jpg", 'wb')
                                fwrite.write(img)
                                fwrite.close()
                                # print("list:" + list)
                        else:
                            params += key + "=" + form.getvalue(key, "") + "\n"
                    print params

            if self.path.startswith("/cgi/"):
                print("dispatcher", self.path)
                dispatcher = Dispatcher(self.path, self, form)
            elif self.path.startswith("/sdkBS/"):
                dispatcher = TpfDispatcher(self, self.path)
            else:
                # 读取相应的静态资源文件，并发送它
                full_file_path = os.curdir + os.sep + self.path
                if os.path.isfile(full_file_path):
                    file_out = open(full_file_path, 'rb')
                    full_text = file_out.read()
                    file_out.close()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    if len(full_text) > 0:
                        self.wfile.write(full_text)
                        print(full_text)
                    else:
                        self.wfile.write(u"{\"resultCode\":1,\"errorCode\":\"10021\",\"desc\":\"描述\"}")
                else:
                    self.send_response(200)
                    self.end_headers()
                    retstr = u"{\"resultCode\":-1,\"errorDesc\":\"请求处理不存在,新建处理\",\"errorCode\":\"err-01\"}"
                    self.wfile.write(retstr)
                    if not os.path.exists(os.path.split(full_file_path)[0]):
                        os.makedirs(os.path.split(full_file_path)[0])
                    fwrite = codecs.open(full_file_path, 'wb', 'utf-8')
                    fwrite.write(retstr)
                    fwrite.close()
                    print retstr, "请求已保存到文件，路径:", full_file_path


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