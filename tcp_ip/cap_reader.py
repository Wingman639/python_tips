#!/usr/bin/python2.5
# -*- coding: utf-8 -*-#
import struct
import os
import re
import sys
import time
import socket


g_big_endian = '>'
g_little_endian = '<'
g_endian = g_big_endian


def Pcap_check(infile):
    c = infile.read(24)
    if not c:
        return c      
    (a,b,cx,d,e,f,g) = struct.unpack(g_endian + 'Ihhiiii',c)
    if a!= 0xA1B2C3D4:
        return False
    print "versionMajor:",b
    print "VersionMinjor:",cx
    print "_TimeZone:",d
    print "_CaptureTimestamp",e
    print "_MaxPacketLength:",f
    print "_LinkLayerType:",g
    return True

def Pcap_read(infile):
    c = infile.read(16)
    if not c:
        return ('', 0, c)      
    (timestamp, millseconds, length, rawlen) = struct.unpack(g_endian + 'IIII',c)
    timeStruct = time.gmtime(timestamp)
    currentTime = (timeStruct.tm_hour * 3600 + timeStruct.tm_min * 60 + 
                    timeStruct.tm_sec) * 1000 + millseconds / 1000
    c = infile.read(34)
    source, dest = struct.unpack(g_endian + '26xII', c)
    source = socket.inet_ntoa(c[26:30])
    dest = socket.inet_ntoa(c[30:])
    infile.read(8)
    c = infile.read(length - 8 - 34)
    return (dest,currentTime,c)



def main():
    fileName = 'block_alarm.cap'
    with open(fileName, 'r') as f:
        if Pcap_check(f):
            reult = Pcap_read(f)
            print reult


if __name__ == '__main__':
    main()