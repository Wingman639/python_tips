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


'''
---------------------
Cap File Head
---------------------
struct pcap_file_header {
    bpf_u_int32     magic;
    u_short         version_major;
    u_short         version_minor;
    bpf_int32       thiszone;       /* gmt to local correction */
    bpf_u_int32     sigfigs;        /* accuracy of timestamps */
    bpf_u_int32     snaplen;        /* max length saved portion of each pkt */
    bpf_u_int32     linktype;       /* data link type (LINKTYPE_*) */
};


---------------------
Frame Head
---------------------
struct pcap_pkthdr {
    struct timeval  ts;             /* time stamp */
    bpf_u_int32     caplen;         /* length of portion present */
    bpf_u_int32     len;            /* length this packet (off wire) */
};


---------------------
Ethernet Packet Head
---------------------
struct EthernetPacket
{
    char            MacDst[6];       ///< 目的网卡物理地址
    char            MacSrc[6];       ///< 源网卡物理地址
    unsigned short  PacketType;      ///< 包类型， ip或ARP等,  PacketType=0x0008是IP包，PacketType=0x0608是ARP包
};
'''


if __name__ == '__main__':
    main()