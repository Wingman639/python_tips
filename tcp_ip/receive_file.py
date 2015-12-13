#!/usr/bin/python2.7
# -*- coding:=utf-8 -*-
 
import socket
import os
import struct
import select
import math
import ConfigParser,string
from optparse import OptionParser
from summd5 import summd5
 
import sys 
reload(sys)
c=sys.getdefaultencoding()
sys.setdefaultencoding('utf-8') 
 
 
 
FileHead=''
FileName=''
FileSize=0
BUFSIZE=0
MD5Name=''
MD5Size=''
Rerecv=0
FLAG=0
 
 
def GetArg():
     p=OptionParser()
     p.add_option('-d',dest='ConfDir',help="the path of the config file:/*/*/*")
     options,args=p.parse_args()
     if not os.path.exists(options.ConfDir):
                print 'the file not exists'
                print "the path of the config file:/*/*/*"
                exit()
     else:
                ConfDir=options.ConfDir
     return ConfDir
      
def ReadConf(ConfDir):
    Addr=()
    cf = ConfigParser.ConfigParser()    
    cf.read(ConfDir)       
    ser_hostname = cf.get("SER", 'HOSTNAME')    
    ser_port= cf.get("SER", "PORT")    
    Addr=(ser_hostname,int(ser_port))
    return Addr
 
def RecvHead(conn):
    global FileHead,BUFSIZE,FileSize,FileName
    FileHead=conn.recv(1024)
    s=FileHead.split("/")
    FileName=s[0].decode('gb2312')
    FileSize=int(s[1])
    BUFSIZE=int(s[2])
    print FileName,FileSize,BUFSIZE
 
 
def Conversation(conn):
    global Rerecv,MD5Name,FileName
    MD5Name='MD5_'+FileName+'.txt'
    Size=struct.calcsize('1i')
    if os.path.isfile(MD5Name):
        Rerecv=1
        print "This is Resend"
    Head=struct.pack('1i',Rerecv)
    conn.send(Head)
     
def Prog(RestSize):
    global FileSize
    RecvSize=FileSize-RestSize
    try:
           a=int(RecvSize*100/float(FileSize))
    except ZeroDivisionError:
           a=0
    sys.stdout.write('----------------------------------Received:'+str(a)+'%'+"\r")
    sys.stdout.flush()
 
def FileRecv(conn,RecvSocket,RestSize):
    global BUFSIZE,FLAG
    try:
         conn.settimeout(1)
         if RestSize>(BUFSIZE+32):
              Rest=BUFSIZE+32
         else:
              Rest=RestSize+32
         c=0
         while Rest!=0:
                s=conn.recv(Rest)
                if c==0:
                    FileData=s
                else:
                    FileData=FileData+s
                Rest=Rest-len(s)                           
                c=c+1
    except socket.timeout:
         print "timeout"
         FLAG=1
          
    return FileData
         
def FirstRecv(conn,RecvSocket):
    global MD5Name,BUFSIZE,FileName,FileSize
    fp=open(FileName,'w')
    RestSize=FileSize
    FLAG=0
    BLOCK=1
    i=0
    fm=open(MD5Name,'w')
    fp.close()
    fm.write(str(BUFSIZE)+'/')
    fm.close()
    while 1:
                fm=open(MD5Name,'ab')
                fp=open(FileName,'ab')
                infds,outfds,errfds=select.select([conn,],[],[],1)
                if len(infds)==0:
                        print "waittime out........"
                        FLAG=1
                        break
                try:
                    FileData=FileRecv(conn,RecvSocket,RestSize)
                except KeyboardInterrupt:
                     FLAG=1
                     break
                w=len(FileData)
                if not FileData or w<32:
                    print RestSize
                    print FileData 
                    break
                RMD5Data=FileData[-32:-1]+FileData[-1]
                FileData=FileData[0:w-32]
                LMD5Data=summd5(FileData)
                if cmp(LMD5Data,RMD5Data) or (not RMD5Data):
                    String='0:'+LMD5Data+'*'
                    fm.write(String)
                else:
                    String=str(BLOCK)+':'+LMD5Data+'*'
                    fp.write(FileData)
                    fm.write(String)
                RestSize=RestSize-len(FileData)
                if RestSize==0:
                    break
                i=i+1
                BLOCK=BLOCK+1
                Prog(RestSize)
                fm.close()
                fp.close()
                 
    fp.close()
    fm.close()
    conn.close()
    RecvSocket.shutdown(socket.SHUT_RD)
    RecvSocket.close()
 
    if FLAG==1 or RestSize!=0:
          print "receive fail!!!"
    else:
          print "Finished "
          os.remove(MD5Name)
                 
def RerecvHead(conn):
    global MD5Name,FileName
    ReFileHead=struct.pack('2i',os.stat(MD5Name).st_size,os.stat(FileName).st_size)
    conn.send(ReFileHead)
    fm=open(MD5Name,'rb')
    while 1:
        MD5Data=fm.read(1024)
        if not MD5Data:
            break
        conn.send(MD5Data)
    fm.close()
     
def ConRecv(conn,RecvSocket):
    global FileName,FileSize,BUFSIZE,MD5Name
    TemFileName='TEM_'+FileName
    TemMD5Name='TEM_'+MD5Name
    fm=open(MD5Name,'rb')
    fp=open(FileName,'rb')
    ft=open(TemFileName,'w')
    c=fm.read()
    c=c.split('/')
    MD5Data=c[1]
    BUFSIZE=int(c[0])
    fm.seek(0)
    ftm=open(TemMD5Name,'w')
    ftm.write(str(BUFSIZE)+'/')
    MD5Data=MD5Data.split("*")
    if not MD5Data[-1]:
        del MD5Data[-1]
    try:
        MD5Data[-1].split(':')
    except ValueError:
        del MD5Data[-1]
    END=len(MD5Data)
    i=0
    ic=0
    RestSize=FileSize-os.stat(FileName).st_size
    FLAG=0
     
    while(1):
         Prog(RestSize)
         infds,outfds,errfds=select.select([conn,],[],[],1)
         if len(infds)==0:
                        print "waittime out........"
                        FLAG=1
                        break
         if i<END:
            CData=MD5Data[i].split(':')
            BLOCK=CData[0]
         else:
            BLOCK='0'
         if BLOCK!='0':
            ft.write(fp.read(BUFSIZE))
            ftm.write(MD5Data[i]+'*')
         else:
             try:
                  
                 FileData=FileRecv(conn,RecvSocket,RestSize)
             except KeyboardInterrupt:
                 FLAG=1
                 break
             w=len(FileData)
             ic=ic+1
             if not FileData or w<32:
                    print "no data"
                    break
             RMD5Data=FileData[-32:-1]+FileData[-1]
             FileData=FileData[0:w-32]
             LMD5Data=summd5(FileData)
             if cmp(LMD5Data,RMD5Data) or (not RMD5Data):
                    String='0:'+LMD5Data+'*'
             else:
                    ft.write(FileData)
                    String=str(BLOCK)+':'+LMD5Data+'*'
 
             ftm.write(String)
             RestSize=RestSize-len(FileData)
             if RestSize<=0:
                print RestSize
                print "restsize==0"
                break
         i=i+1
          
    if RestSize>0:
        s=fp.read()
        ft.write(s)
        while i<len(MD5Data):
            ftm.write(MD5Data[i])
            i=i+1
    ftm.close()
    fp.close()
    fm.close()
    ft.close()
    conn.close()
    os.remove(FileName)
    os.remove(MD5Name)
    os.rename(TemFileName,FileName)
    os.rename(TemMD5Name,MD5Name)
    RecvSocket.shutdown(socket.SHUT_RD)
    RecvSocket.close()
    if FLAG==1 or RestSize!=0:
          print "receive fail!!!"
    else:
          print "Finished "
          os.remove(MD5Name)
           
     
         
                  
def Recv(ConfDir):
    Addr=()
    Addr=ReadConf(ConfDir)
    RecvSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    RecvSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    RecvSocket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,8888888)
    RecvSocket.bind(Addr)
    RecvSocket.listen(5)
    print "waiting..................."
    conn,addr=RecvSocket.accept()
 
    print "send from:",addr
    RecvHead(conn)
    Conversation(conn)
    if Rerecv==0:
        FirstRecv(conn,RecvSocket)
    else:
        RerecvHead(conn)
        ConRecv(conn,RecvSocket)
         
 
 
if __name__=='__main__':
        ConfDir=GetArg()
        Recv(ConfDir)