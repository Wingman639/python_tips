import sys
import socket
import threading
from binascii import hexlify
import paramiko


class SSHServer(paramiko.ServerInterface):
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

    # def check_auth_gssapi_keyex(self, username,
    #                             gss_authenticated=paramiko.AUTH_FAILED,
    #                             cc_file=None):
    #     return paramiko.AUTH_SUCCESSFUL

    # def check_auth_gssapi_with_mic(self, username,
    #                                gss_authenticated=paramiko.AUTH_FAILED,
    #                                cc_file=None):
    #     return paramiko.AUTH_SUCCESSFUL

    # def check_auth_publickey(self, username, key):
    #     return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

port = 2200

paramiko.util.log_to_file('ssh_server_simple.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')

print('Read key: ' + paramiko.py3compat.u(hexlify(host_key.get_fingerprint())))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))
sock.listen(100)
print('listening at %d ...' % port)
client, addr = sock.accept()
print 'Client coming: ', addr

with paramiko.Transport(client, gss_kex=False) as t:
    t.add_server_key(host_key)
    server = SSHServer()
    t.start_server(server=server)
    with t.accept(20) as chan:
        if chan is None:
            print('no channel.')
            sys.exit(1)
        print('Authrized.')

        server.event.wait(10)
        if not server.event.is_set():
            print('*** Client never asked for a shell.')
            sys.exit(1)

        chan.send('\r\nWelcome to my server.\r\n')
        chan.send('>')
        f = chan.makefile('rU') 
        cmd = f.readline().strip('\r\n')
        chan.send('\r\nreceived: ')
        chan.send(cmd)
        chan.send('\r\n')









