import SocketServer
from multiprocessing.dummy import Pool as ThreadPool

class TransTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "Trans {} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class OamTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "OAM {} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

def start_server(port):
    HOST = "0.0.0.0"
    server = SocketServer.TCPServer((HOST, port), TransTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    pool = ThreadPool(3)
    ports = [9999, 9001, 9002]
    pool.map(start_server, ports)
    pool.close()
    pool.join()



