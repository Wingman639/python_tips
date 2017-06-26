import sys
import socket
import threading
from binascii import hexlify
import paramiko
import time

PROMPT = '>'

class SSHServerIf(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True

    def check_auth_password(self, username, password):
        if (username == password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


class SSHServerControler(object):
    def __init__(self, port=2200, key_file='server_rsa.key'):
        self.port = port
        self.host_key = paramiko.RSAKey(filename=key_file)
        print('Read key: ' + paramiko.py3compat.u(hexlify(self.host_key.get_fingerprint())))
        self.stop = None

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(100)
        print('listening at %d ...' % self.port)
        client, addr = sock.accept()
        print 'Client coming: ', addr

        with paramiko.Transport(client, gss_kex=False) as transport:
            transport.add_server_key(self.host_key)
            server = SSHServerIf()
            transport.start_server(server=server)
            self.accept_connection(server, transport)

    def accept_connection(self, server, transport):
        with transport.accept(20) as chan:
            if chan is None:
                print('no channel.')
                sys.exit(1)
            print('Authrized.')

            server.event.wait(10)
            if not server.event.is_set():
                print('*** Client never asked for a shell.')
                sys.exit(1)

            chan.send('\r\nWelcome to my server.\r\n')
            chan.send(PROMPT)
            self.receive(chan)



    def receive(self, chan):
        in_f = chan.makefile('rU')
        self.stop = False
        while not self.stop:
            line = self.receive_line(chan, in_f)
            # line = in_f.readline().strip('\r\n')
            print line
            chan.send('\n\r' + PROMPT)
            if 'exit' == line.strip('\n\r'):
                self.stop = True
                break
            time.sleep(0.01)


    def receive_line(self, chan, in_f):
        line = ''
        c = ''
        while not self.stop and '\n' not in c and '\r' not in c:
            c = self.receive_c(chan, in_f)
            line += c
            time.sleep(0.01)
        return line


    def receive_c(self, chan, in_f):
        c = in_f.read(1)
        if c:
            chan.send(c)
        return c

    def stop(self):
        self.stop = True


if __name__ == '__main__':


    paramiko.util.log_to_file('ssh_server_simple.log')
    controller = SSHServerControler()
    controller.run()






