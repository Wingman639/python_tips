# -*- coding: cp936 -*-
from socket import *
import struct
import os

ratio_base = 0.00


def print_ratio(ratio, delta=1.00):
    global ratio_base
    if ratio > ratio_base + delta:
        ratio_base = ratio_base + delta
        print " %4.2f" % ratio,
        print "%"
    else:
        pass


def client_sender():
    print "current directory : ", os.getcwd()

    server_ip = raw_input("receiver's ip : ")
    server_port = raw_input("receiver's port : ")

    ADDR = (server_ip, int(server_port))
    BUFSIZE = 1024
    FILEINFO_SIZE = struct.calcsize('128s32sI8s')

    while True:
        try:
            filename = raw_input("file to be sent under this dir: ")
            fhead = struct.pack('128s11I',
                                filename,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                os.stat(filename).st_size,
                                0, 0)
            sendSock = socket(AF_INET, SOCK_STREAM)
            sendSock.connect(ADDR)
            sendSock.send(fhead)
            fp = open(filename, 'rb')
            while True:
                filedata = fp.read(BUFSIZE)
                if not filedata:
                    break
                sendSock.send(filedata)
            fp.close()
            print "sent"
        except:
            print "sent error"

    sendSock.close()


def server_receiver():
    print "my ip : (ipconfig / ifconfig)"
    server_port = raw_input("my port : ")
    print "waiting for file ..."

    ADDR = ("", int(server_port))
    BUFSIZE = 1024
    FILEINFO_SIZE = struct.calcsize('128s32sI8s')
    recvSock = socket(AF_INET, SOCK_STREAM)
    recvSock.bind(ADDR)
    recvSock.listen(5)

    while True:
        try:
            conn, addr = recvSock.accept()
            fhead = conn.recv(FILEINFO_SIZE)
            filename, temp1, filesize, temp2 = struct.unpack('128s32sI8s', fhead)
            filename = filename.strip('\00')

            if os.path.isfile(filename):
                filename = raw_input("文件已存在，请起一个新名字[default: new_%s]" % filename)
                if filename.strip() == "":
                    filename = 'new_'+filename.strip('\00')
                else:
                    filename = filename.strip('\00')
            fp = open(filename, 'wb')
            restsize = filesize
            while True:
                if restsize > BUFSIZE:
                    filedata = conn.recv(BUFSIZE)
                else:
                    filedata = conn.recv(restsize)
                if not filedata:
                    break
                fp.write(filedata)
                restsize = restsize-len(filedata)
                ratio = ( float(filesize) - float(restsize) ) / float(filesize) * 100
                print_ratio(ratio)
                if restsize == 0:
                    break
            fp.close()
            conn.close()
            print filename, " received"
        except:
            print "receive error"

    recvSock.close()

if __name__ == "__main__":
    choice = raw_input("send or receive [s/r] : ")
    if choice == "s":
        client_sender()
        print
    elif choice == "r":
        server_receiver()
        print
    else:
        print "oops..."
