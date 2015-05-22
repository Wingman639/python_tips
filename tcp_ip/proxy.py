import SocketServer
import thread

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
        

def new_server(para_dict):
    HOST = "0.0.0.0"
    port = para_dict['port']
    handler_class = para_dict['handler_class']
    server = SocketServer.TCPServer((HOST, port), handler_class)
    return server
    

if __name__ == "__main__":
    ports = { 
             '9001' : {'port':9001, 'handler_class':TransTCPHandler, 'server':None},
             '9002' : {'port':9002, 'handler_class':TransTCPHandler, 'server':None},
            }
    oam_server = new_server({'port':9999, 'handler_class':OamTCPHandler})
    thread.start_new_thread(oam_server.serve_forever, ())
    for port_dict in ports.values():
        server = new_server(port_dict)
        port_dict['server'] = server
        server_thread = thread.start_new_thread(server.serve_forever, ())
    



