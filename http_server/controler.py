#-*-coding:UTF-8-*-

'''
This http server controler is used to start and stop service of a server based on BaseHTTPServer.
With this controler, functional test case is able to start and stop supporting service at any time.
'''

import threading

class ServerStartThread (threading.Thread):
    def __init__(self, http_server):
        threading.Thread.__init__(self)
        self.http_server = http_server

    def run(self):
        print "Starting... "
        self.http_server.serve_forever()
        print "Exiting Start Thread "


class ServerStopThread (threading.Thread):
    def __init__(self, http_server):
        threading.Thread.__init__(self)
        self.http_server = http_server

    def run(self):
        print "Shutting Down... "
        self.http_server.shutdown()
        print "Exiting Stop Thread"


class Controler(object):
    def __init__(self, http_server):
        self.http_server = http_server

    def start_service(self):
        ServerStartThread(self.http_server).start()

    def stop_service(self):
        ServerStopThread(self.http_server).start()


if __name__ == '__main__':
    import time
    from basic_http_server import MyRequestHandler, HTTPServer
    ip = '127.0.0.1'
    port = 8000

    def test_server_start_wait_seconds_then_stop():
        http_server = HTTPServer((ip, int(port)), MyRequestHandler)
        controler = Controler(http_server)
        controler.start_service()
        time.sleep(2)
        controler.stop_service()


    def main():
        test_server_start_wait_seconds_then_stop()

    main()