# encoding: utf-8

from cmd import Cmd
import sys

class CmdTest(Cmd):

    def __init__(self):            #初始基础类方法
        Cmd.__init__(self)

    def help_hello(self):
        print("输入hello 参数，将执行o_hello方法，输出参数值")

    def do_hello(self,line):
        print("do_hello:",line)

    def help_exit(self):          #以help_*开头的为帮助
        print("输入exit退出程序")

    def do_exit(self,line):       #以do_*开头为命令
        print("Exit:",line)
        sys.exit()

if __name__ =="__main__":
    cmd=CmdTest()
    cmd.cmdloop()
