import select
import socket
import time
import threading
import sys
from collections import deque
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, \
     ENOTCONN, ESHUTDOWN, EINTR, EISCONN, EBADF, ECONNABORTED, EPIPE, \
     errorcode

inBufSize = 4096
outBufSize = 4096


class ExitNow(Exception):
    pass

_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN,
                           ECONNABORTED, EPIPE, EBADF))
_bubbleExceptions = (ExitNow, KeyboardInterrupt, SystemExit)


# A server with unblocking multitargets communication
class ChatServer(threading.Thread):
    def __init__(self, name, port=5247):
        threading.Thread.__init__(self)
        self.daemon = True
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listen(5)
        self.socketsMap = {self.serverSocket: self}

        self.name = name
        self.port = port

    def poll(self):
        r, w, e = [], [], []
        for sock, session in self.socketsMap.items():
            readable = session.readable()
            writable = session.writable()
            if readable:
                r.append(sock)
            if writable:
                w.append(sock)
            if readable or writable:
                e.append(sock)

        if r == w == e == []:
            time.sleep(3)
            return

        try:
            r, w, e = select.select(r, w, e, 1.5)
        except select.error, e:
            if e.args[0] != EINTR:
                raise
            else:
                return

        for sock in r:
            session = self.socketsMap.get(sock)
            if session is None:
                continue
            try:
                session.onRead()
            except _bubbleExceptions:
                raise
            except e:
                print e
                session.handlerError()

        for sock in w:
            session = self.socketsMap.get(sock)
            if session is None:
                continue
            try:
                session.onWrite()
            except _bubbleExceptions:
                raise
            except:
                session.handlerError()

        for sock in e:
            session = self.socketsMap.get(sock)
            if session is None:
                continue
            try:
                session.onException()
            except _bubbleExceptions:
                raise
            except:
                session.handlerError()

    def run(self):
        print 'Server Start'
        while self.socketsMap:
            self.poll()
        print 'Server Down'

    def readable(self):
        return True

    def writable(self):
        return False

    def onRead(self):
        self._onRead()

    def _onRead(self):
        newSocket, address = self.serverSocket.accept()
        try:
            name = newSocket.recv(1024)
            newSocket.send(self.name)
            if not name:
                return
        except socket.error, e:
            if e.args[0] in _DISCONNECTED:
                newSocket.close()
                return
            else:
                raise
        if self.isAccept(name, address[0]):
            ChatSession(self, newSocket, name)

    def isAccept(self, name, address):
        return True


# A wrapper of socket,
# introducing some protections and compatibility to ChatServer
class Session:
    def __init__(self, server, sock):
        self.server = server
        self.socket = sock
        self.id = self.socket.fileno()
        self.addToServer(self.server)

        # self.socket.setblocking(0)
        self.connected = True

        try:
            self.remoteAddress = sock.getpeername()
        except socket.error, err:
            if err.args[0] in (ENOTCONN, EINVAL):
                self.connected = False
            else:
                self.delFromServer(self.server)
                raise

    def addToServer(self, s):
        s.socketsMap[self.socket] = self

    def delFromServer(self, s):
        try:
            s.socketsMap.pop(self.socket)
        except:
            pass

    def __repr__(self):
        status = [self.__class__.__module__+"."+self.__class__.__name__]
        if self.connected:
            status.append('connected')
        if self.remoteAddress is not None:
            try:
                status.append('%s:%d' % self.remoteAddress)
            except TypeError:
                status.append(repr(self.remoteAddress))
        return '<%s at %#x>' % (' '.join(status), id(self))

    def readable(self):
        return True

    def writable(self):
        return True

    def connect(self, address):
        self.connected = False
        self.connecting = True
        err = self.socket.connect_ex(address)
        if err in (EINPROGRESS, EALREADY, EWOULDBLOCK, EINVAL):
            self.address = address
            self.send(self.server.name)
            return self.recv(1024)
        if err in (0, EISCONN):
            self.address = address
            self.send(self.server.name)
            return self.recv(1024)
        else:
            raise socket.error(err, errorcode[err])

    def close(self):
        self._close()

    def _close(self):
        self.connected = False
        self.connecting = False
        self.delFromServer(self.server)
        try:
            self.socket.close()
        except socket.error, e:
            if e.args[0] not in (ENOTCONN, EBADF):
                raise

    def log(self, message):
        sys.stderr.write('log: %s\n' % str(message))

    def send(self, data):
        try:
            result = self.socket.send(data)
            return result
        except socket.error, why:
            if why.args[0] == EWOULDBLOCK:
                return 0
            elif why.args[0] in _DISCONNECTED:
                self.close()
                return 0
            else:
                raise

    def recv(self, buffer_size):
        try:
            data = self.socket.recv(buffer_size)
            if not data:
                self.close()
                return ''
            else:
                return data
        except socket.error, why:
            if why.args[0] in _DISCONNECTED:
                self.close()
                return ''
            else:
                raise

    def onRead(self):
        if not self.connected:
            if self.connecting:
                self.onConnect()
            self.handleRead()
        else:
            self.handleRead()

    def onWrite(self):
        if not self.connected:
            if self.connecting:
                self.onConnect()
        self.handleWrite()

    def onConnect(self):
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            raise socket.error(err)
        self.handleConnect()
        self.connected = True
        self.connecting = False

    def onException(self):
        print 'a'
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            self.close()
        else:
            self.handleException()

    def handleError(self):
        print 'error!!!'

    def handleException(self):
        pass

    def handleRead(self):
        pass

    def handleWrite(self):
        pass

    def handleConnect(self):
        pass


# having the basic name;time;message sending and receiving
class ChatSession(Session):
    endTag = '<<.end>>'
    splitTag = '<<.split>>'

    def __init__(self, server, sock, remoteName=None):
        Session.__init__(self, server, sock)
        self.name = server.name
        self.inBuf = ''
        self.outQueue = deque()
        self.remoteName = remoteName

    def push(self, data):
        t = time.strftime('%m-%d %H:%M:%S', time.localtime())
        data = self.splitTag.join((self.name, t, data))
        if data.find(self.endTag) == -1:
            self.processOutMessage(data)
            data = self.endTag.join((data, ''))
            if len(data) > outBufSize:
                for i in xrange(0, len(data), outBufSize):
                    self.outQueue.append(data[i:i+outBufSize])
            else:
                self.outQueue.append(data)
            return True
        else:
            return False

    def connect(self, address):
        self.remoteName = Session.connect(self, address)

    def processInMessage(self, message):
        name, time, text = message.split(self.splitTag)
        self.printMessage(name, time, text)

    def processOutMessage(self, message):
        pass

    def printMessage(self, name, time, text, out=False):
        print '%s said at %s\n  %s' % (name, time, text)

    def readable(self):
        return True

    def writable(self):
        return len(self.outQueue)

    def handleRead(self):
        try:
            data = self.recv(inBufSize)
        except socket.error, e:
            self.handleError()
            return

        self.inBuf += data

        while self.inBuf:
            spl = self.endTag
            splLen = len(spl)
            index = self.inBuf.find(spl)
            if index != -1:
                if index > 0:
                    self.processInMessage(self.inBuf[:index])
                self.inBuf = self.inBuf[index+splLen:]
                return True
            else:
                break
        return False

    def handleWrite(self):
        while self.outQueue and self.connected:
            m = self.outQueue[0]
            if not m:
                del self.outQueue[0]
                if m is None:
                    self.close()
                    return

            try:
                check = self.send(m)
            except socket.error:
                self.handleError()
                return

            if check:
                if check < len(m):
                    self.outQueue[0] = m[check:]
                else:
                    del self.outQueue[0]

    def end(self):
        self.outQueue.append(None)


def find_prefix_at_end(haystack, needle):
    l = len(needle) - 1
    while l and not haystack.endswith(needle[:l]):
        l -= 1
    return l


if __name__ == '__main__':
    s = ChatServer('testServer', 5247)
    s.start()
    while 1:
        a = raw_input()
