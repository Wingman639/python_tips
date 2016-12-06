# -*-coding:UTF-8-*-
'''
HTTP server for testing, support: GET, POST.

NOTICE: only ASCII is supported
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io
import shutil
import urllib
import os
import sys
import json
import threading
import ssl

current_dir = os.path.dirname(__file__)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        mpath, margs = urllib.splitquery(self.path)
        self.send_json_response({'method':'GET',
                                 'path':self.path,
                                 'mpath':mpath,
                                 'margs':margs})

    def do_POST(self):
        mpath, margs = urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.send_json_response({'method':'POST',
                                 'path': self.path,
                                 'data': datas,
                                 'mpath':mpath,
                                 'margs':margs})

    def do_DELETE(self):
        mpath, margs = urllib.splitquery(self.path)
        self.send_json_response({'method':'DELETE',
                                 'path':self.path,
                                 'mpath':mpath,
                                 'margs':margs})

    def do_PATCH(self):
        mpath, margs = urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.send_json_response({'method':'PATCH',
                                 'path': self.path,
                                 'data': datas,
                                 'mpath':mpath,
                                 'margs':margs})


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


def get_server(ip, port, https=False):
    if https:
        return https_server(ip, port)
    else:
        return http_server(ip, port)


def http_server(ip, port):
    return HTTPServer((ip, int(port)), RequestHandler)


def https_server(ip, port=443):
    http_server = HTTPServer((ip, int(port)), RequestHandler)
    http_server.socket = ssl.wrap_socket (http_server.socket,
                                        keyfile=os.path.join(current_dir, 'server.key'),
                                        certfile=os.path.join(current_dir, 'local_cert.pem'),
                                        server_side=True)
    return http_server


if __name__ == '__main__':
    import time
    ip = '127.0.0.1'
    port = 8000

    def test():
        print 'Server start...(you can stop it with Ctrl+C)'
        http_server = get_server(ip, port)
        http_server.serve_forever()

    def test_https():
        print 'HTTPS server start...(you can stop it with Ctrl+C)'
        http_server = get_server(ip, port=port, https=True)
        http_server.serve_forever()

    test()
    #test_https()