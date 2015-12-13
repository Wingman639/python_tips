from optparse import OptionParser
import sys
import os
import re
import time
 
import socket
import struct
import select
from summd5 import summd5#导入计算被发送文件md5值的文件
 
import sys 
reload(sys)
c=sys.getdefaultencoding()
sys.setdefaultencoding('utf-8') #被发送文件名中带有汉字的文件
 
 
 
FileName='' #被发送文件名
FileDir=''  #被发送文件的位置
BLOCKSIZE=0 #被发送文件的分块大小
Resend=0    #续传标志
FLAG=0      #发送成功标志
MD5Name=''  #被发送文件的MD5文件的名称
MD5Size=0   #被发送文件的MD5文件大小
SendSize=0 
 
#---------函数名：SetBuffer
#---------函数功能：用于设置socket发送缓存区的最大容量，固定为：8888888B
#---------调用函数：Send(Addr)
#---------被调用函数：
#---------输入参数：SendSocket发送文件刚开始创建的套接字
#---------返回值：
def SetBuffer(SendSocket):
        SendSize=8888888; 
        SendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,SendSize)
 
 
#---------函数名：GetArgs()
#---------函数功能：用于获取处理命令行参数
#---------调用函数：
#---------被调用函数：
#---------输入参数：
#---------返回参数：Addr 发送目的主机的IP地址和端口
def GetArgs():
        global FileName,FileDir,BLOCKSIZE
        p=OptionParser() #构建OptionParser解析模块的对象
 
        #向OptionParser对象中添加Option
 
        #增加Addr选项，解析要发送的目的IP地址和端口，命令行格式为：-a 10.65.10.79,8000
        p.add_option('-a',dest='Addr',help="the Receiver's IP Address and Port,eg:'10.65.10.79',80",default='')
 
        #增加FileDir选项，解析要发送的文件的位置，命令行格式为：-d /*/*/filename
        p.add_option('-d',dest='FileDir',help="the path of the flie to be senteg:/*/*/*")
 
        #增加BLOCKSIZE选项，解析要发送的文件的分块大小，命令行格式为：-b 整数 范围(0,8888888)，默认值：4096
        p.add_option('-b',dest='BLOCKSIZE',help='the size of the block(0,8888888)',default=4096)
        options,args=p.parse_args()#调用OptionParser的解析函数
         
        if not options.Addr:#Addr参数不能为空
                print "please input Addr"
                exit()
        Ad=re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\,\d{0,65535}',options.Addr)#对Addr参数进行正则匹配
        if not Ad:#对于Addr的非法输入进行提示
                print 'invalid Address Arguments'
                print "the Receiver's IP Address and Port,eg:'10.65.10.79',8000"
        else:
                c=Ad.group().split(',')
                Addr=(c[0],int(c[1]))#把IP地址和端口格式为建立socket所需的格式
        if not os.path.exists(options.FileDir):#对于非法的文件目录进行提示
                print 'the file not exists'
                print "the path of the flie to be senteg:/*/*/*"
                exit()
        else:
                FileDir=options.FileDir
        BLOCKSIZE=int(options.BLOCKSIZE)#把分块参数由字符串转化为整数
        if BLOCKSIZE<0 or BLOCKSIZE>8888888:#对于非法的分块参数进行提示
                print 'the BLOCKSIZE is invalid'
                print 'please input number in (0,65536)'
                exit()
        return Addr
 
 
#---------函数名：SendHead(SendSocket,Addr)
#---------函数功能：用于发送文件头信息，包括文件名，文件大小和分块大小
#---------调用函数：Send(Addr)
#---------被调用函数：
#---------输入参数：SendSocket,Addr:建立的socket套接字和目的主机的地址
#---------返回参数：              
def SendHead(SendSocket,Addr):
        global FileName,BLOCKSIZE
        FileName=FileDir.split('/')
        FileName=FileName[-1]
        FileName.decode('gb2312')#用于处理发送的文件名中包括汉字的情况
        String=FileName+'/'+str(os.stat(FileDir).st_size)+'/'+str(BLOCKSIZE)
        print String
        try:
                 SendSocket.send(String)#发送文件头信息
        except socket.error,arg:#出错处理
                (errno,err_msg)=arg
                print "Send faild!error:%s,errno=%d" %(err_msg,errno)
                exit()
 
 
#---------函数名：Conversation(SendSocket)
#---------函数功能：用于进行发前回话，接收由接收方返回的续发标志。
#---------调用函数：Send(Addr)
#---------被调用函数：
#---------输入参数：SendSocket:建立的socket套接字
#---------返回参数：          
def Conversation(SendSocket):
        global Resend
        Size=struct.calcsize('1i')#在python socket传输时，发端把python的数值类型用struct.pack
                                  #根据格式符转换为字符串（相当于字节流），以便于在网络上进行传输
                                  #收端用struct.unpack把接收到的字节流转换为python的数据类型，返回值为一个元祖
                                  #此处用struct.calcsize计算格式字符的大小。
        try:    
                 Head = SendSocket.recv(Size)
                 s=struct.unpack('1i',Head)
                 Resend=s[0] #给Resend续传标志1赋值
        except socket.error,arg:
                (errno,err_msg)=arg
                print "send failed !error:%s,errno=%d" %(err_msg,errno)
 
 
#---------函数名：Prog()
#---------函数功能：用于在命令行终端显示发送文件的进度信息
#---------调用函数：SendFile(SendSocket)
#                  ConSend(SendSocket)
#---------被调用函数：
#---------输入参数：
#---------返回参数：          
    
def Prog():
        global SendSize
        FileSize=os.stat(FileDir).st_size
        try:
           a=int(SendSize*100/float(FileSize))#计算发送文件的进度百分比
        except ZeroDivisionError:
           a=0
        sys.stdout.write('----------------------------------Send:'+str(a)+'%'+"\r")#显示进度信息
        sys.stdout.flush()
 
 
 
#---------函数名：SendFile(SendSocket)
#---------函数功能：用于初次发送文件，从文件中一次读取出给的分块大小的内容，然后计算md5值，
#                  把要发的文件内容+相应的md5数据字符串，发送给接收端        
#                  由收端来分块进行md5校验来计算文件是否完整正确的接收。        
#---------调用函数：Send(Addr)
#---------被调用函数：summd5(FileData)
#                    Prog()
#---------输入参数：SendSocket:建立的socket套接字
#---------返回参数：                      
def SendFile(SendSocket):
        global FLAG,BlOCKSIZE,FileDir,SendSize
        s=FileDir.split('/')
        FileName=s[-1]#解析文件目录参数，给文件名参数赋值
        fp=open(FileDir,'rb')
        i=0
        while 1:
            i=i+1
            FileData=fp.read(BLOCKSIZE)#从要发的文件中读取相应分块大小的内容
            if not FileData: break
            Md5Data=summd5(FileData)#计算相应分块大小内用的md5数据
            FileData=FileData+Md5Data
            try:
                s=SendSocket.send(FileData)
                SendSize=SendSize+s
            except:
                (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                (error,err_msg)=ErrorValue
                print "Send failed %s error:%s"%(err_msg,error)
                FLAG=1
                break
            Prog()#显示文件发送进度
        
        fp.close()
        if FLAG==0:
                    print '**-------------Send %s Successfully-----------**'%(FileName)
                    return 0
        else:
 
                print '**----------------Send failed----------------**'
         
         
 
#---------函数名：ResendHead(SendSocket)
#---------函数功能：接收用于续传文件时的文件头信息,包括已发送文件的大小
#---------调用函数：Send(Addr)
#---------被调用函数：
#---------输入参数：SendSocket:创建的socket套接字
#---------返回参数：         
def ResendHead(SendSocket):
        global MD5Size,SendSize
        Size=struct.calcsize('2i')
        ResendHead=SendSocket.recv(Size)
        MD5Size,SendSize=struct.unpack('2i',ResendHead)
        print "sendsize",SendSize
     
 
 
#---------函数名：RecvMD5(SendSocket)
#---------函数功能：在文件续传的情况下，接收由发送端发来的上次接收文件的md5文件。
#---------调用函数：Send(Addr)
#---------被调用函数：
#---------输入参数：SendSocket:创建的socket套接字
#---------返回参数：
def RecvMD5(SendSocket):
        global MD5Name,MD5Size,BLOCKSIZE,FileName
        MD5Name='MD5_'+FileName+'.txt'#新建md5文件
        fw=open(MD5Name,'w')
        RestSize=MD5Size
        i=0
        while 1:
            infds,outfds,errfds=select.select([SendSocket,],[],[],5)
            if len(infds)==0:  #用于处理等待超时的情况
                print "waitting time out!!!!"
                exit;
            if RestSize<1024:
                ReFileData=SendSocket.recv(RestSize)
            else:
                ReFileData=SendSocket.recv(1024)
             
            if not ReFileData:
                                print "not data"
                                break
            RestSize=RestSize-len(ReFileData)
            if i==0:
                    s=ReFileData.split('/')
                    print s[0]
                    BLOCKSIZE=int(s[0])
                    print "this is Resend ,the blocksize is :",BLOCKSIZE
                    ReFileData=s[1]
            fw.write(ReFileData)
            if RestSize==0:
                                print "size 0"
 
                                break
            i=i+1
        print "md5 received"
        fw.close()
 
 
#---------函数名：RecvMD5(SendSocket)
#---------函数功能：文件续传，根据收到的md5文件，对文件进行有选择的发送，当md5的块号为0时，重发此块文件，
#                  当块号不为0时，跳过，同时调用进度显示
#---------调用函数：Send(Addr)
#---------被调用函数：Prog()
#---------输入参数：SendSocket:创建的socket套接字
#---------返回参数：
def ConSend(SendSocket):
        global MD5Name,FileName,BLOCKSIZE,FileDir,SendSize,FLAG
        SendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,8000000)#设置发送区大小
        fw=open(MD5Name,'rb')
        fp=open(FileDir,'rb')
        MD5Data=fw.read()
 
        #解析md5文件，对于文件末尾有md5数据格式不全的情况，删除，找出最后一个md5数据的块数序号
        MD5Data=MD5Data.split("*")
        if not MD5Data[-1]:
                del MD5Data[-1]
        try:
               MD5Data[-1].split(":")
        except ValueError:
               del MD5Data[-1]
        END=len(MD5Data)
        i=0
        while 1:
            Prog()#显示发送进度信息
            if i < END:
                CData=MD5Data[i].split(":")
                BLOCK=CData[0]
            else:
                BLOCK='0'
            i=i+1
            if BLOCK!='0':#当块数序号不为0时，跳过不发。
                fp.seek(BLOCKSIZE,1)
            else:         #当块数序号为0时，发送此块文件内容。
                FileData=fp.read(BLOCKSIZE)
                if not FileData:break
                SMD5Data=summd5(FileData)
                FileData=FileData+SMD5Data
                try:
                        
                       s=SendSocket.send(FileData)
                       SendSize=SendSize+s
                except socket.error,arg:
                        fw.close()
                        fp.close()
                        (errno,err_msg)=arg
                        print "Send failed!error:%s,errno=%d" %(err_msg,errno)
                        FLAG=1
                        break
           
        if FLAG==0:
                    print '**-------------Send %s Successfully-----------**'%(FileName)
                    return 0
        else:
 
                print '**----------------Send failed----------------**'
         
 
        fw.close()
        fp.close()
        os.remove(MD5Name)#删除接收的md5文件
 
 
#---------函数名：Send(Addr)
#---------函数功能：发送文件函数
#---------调用函数：
#---------被调用函数： SetBuffer(SendSocket)
#                     SendHead(SendSocket,Addr)
#                     Conversation(SendSocket)
#                     SendFile(SendSocket)
#                     ResendHead(SendSocket)
#                     RecvMD5(SendSocket)
#                     ConSend(SendSocket)
#---------输入参数：Addr，命令行输入的发送目的主机的IP地址和端口
#---------返回参数：        
def Send(Addr):
        SendSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#建立套接字
        SendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,8000)
        SendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,8000)
        SetBuffer(SendSocket)#设置发送缓冲区大小
        try:
                 SendSocket.connect(Addr)
        except socket.error,arg:
                (errno,err_msg)=arg
                print "Send failed!error:%s,errno=%d" %(err_msg,errno)
        SendHead(SendSocket,Addr)#发送文件头信息
        Conversation(SendSocket)#发前续传会话，用来判断此次为初次发送还是文件续传
        if Resend==0:
                SendFile(SendSocket)#为初次发送
        else:
                ResendHead(SendSocket)#进行续传，先发送续传头文件
                RecvMD5(SendSocket)#接收由接收方发来的上次接收文件的md5文件
                ConSend(SendSocket)#文件续传
        SendSocket.close()#关闭套接字
         
         
                
if __name__=='__main__':
        Addr=GetArgs()#获取解析命令行参数
        if Addr:
                Send(Addr)