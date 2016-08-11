#encoding=utf-8
'''
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io,shutil
import urllib
import os, sys

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        mpath,margs=urllib.splitquery(self.path) # ?分割
        self.do_action(mpath, margs)

    def do_POST(self):
        mpath,margs=urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.do_action(mpath, datas)

    def do_action(self, path, args):
        self.outputtxt(str(path) + ':' + str(args))

    def outputtxt(self, content):
        #指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

def start_server(ip, port):
    print 'server (%s, %s) start...' % (ip, str(port))
    http_server = HTTPServer((ip, int(port)), MyRequestHandler)
    http_server.serve_forever() #设置一直监听并接收请求

if __name__ == '__main__':
    def main():
        start_server('127.0.0.1', 8000)
    main()