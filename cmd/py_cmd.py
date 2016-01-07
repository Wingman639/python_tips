#coding:utf-8
"""
实现python操作cmd
以及与windows系统交互
"""
import os, sys, subprocess

p = subprocess.Popen('python in.py',
					shell=False,
					stdin=subprocess.PIPE,
					#stdout=subprocess.PIPE,
					#stderr=subprocess.PIPE
					)
output, error = p.communicate(input='y\nyes\n')
#print output
#print error
