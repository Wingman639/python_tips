# -*-coding:UTF-8-*-

'''
curl -X POST -H "Content-Type: multipart/form-data" -F "content=@1.zip" http://localhost:8000/
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io
import shutil
import urllib
import os
import sys
import json
import re
import posixpath
import platform

current_dir = os.path.dirname(__file__)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        mpath, margs = urllib.splitquery(self.path)
        (succeed, result) = self.deal_post_data()
        self.send_json_response({'method':'POST',
                                 'succeed': succeed,
                                 'result': result})

    def send_json_response(self, a_dict):
        print a_dict
        json_text = json.dumps(a_dict)
        f = io.BytesIO()
        f.write(json_text)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(json_text)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)


    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        print boundary
        remainbytes = int(self.headers['content-length'])
        print remainbytes
        line = self.rfile.readline()
        print line
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        print line
        remainbytes -= len(line)
        # fn = re.findall(r'Content-Disposition:[\w\-\;\s]*?name="file|content"; filename="(.*)"', line)
        fn = re.findall(r'Content-Disposition:[\w\-\;\s\"\=]*? filename="(.*)"', line)
        print fn
        if not fn:
            return (False, "Can't find out file name...")
        # path = self.translate_path(self.path)
        # print path
        # osType = platform.system()
        # try:
        #     if osType == "Linux":
        #         fn = os.path.join(path, fn[0].decode('gbk').encode('utf-8'))
        #     else:
        #         fn = os.path.join(path, fn[0])
        # except Exception, e:
        #     return (False, "Only ASCII file name is supported.")
        # while os.path.exists(fn):
        #     fn += "_"
        fn = fn[0]
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

def http_server(ip, port):
    return HTTPServer((ip, int(port)), RequestHandler)


if __name__ == '__main__':
    import time
    ip = '127.0.0.1'
    port = 8083

    def test():
        print 'Server start %s:%d...(you can stop it with Ctrl+C)' %(ip, port)
        server = http_server(ip, port)
        server.serve_forever()

    test()
