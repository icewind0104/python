#!/usr/bin/python3

import socket, struct, os, time, array

def __checksum(packet):
    if len(packet) & 1:
        packet = packet + '\0'
    words = array.array('h', packet)
    sum = 0
    for word in words:
        sum += (word & 0xffff)
        if sum >> 16:
            sum = (sum >> 16) + (sum & 0xffff)
    return (~sum) & 0xffff

def ping(ip, n=1, timeout=3):
    if n < 1 or not isinstance(n, int):
        raise ValueError ('Param(n) is illigel')
    if timeout < 0:
        raise ValueError ('param(timeout) can`t less than 0')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    header = struct.pack('bbHHh', 8, 0, 0, os.getpid(), 0)
    data = struct.pack('d', time.time())
    packet = header + data
    chksum = __checksum(packet)
    icmpPacket = struct.pack('bbHHh', 8, 0, chksum, os.getpid(), 0) + data
    sock.settimeout(timeout)
    r = []
    for i in range(n):
        Stime = time.time()
        sock.sendto(icmpPacket, (ip, 0))
        try:
            string =  sock.recvfrom(1024)[1][0]
        except socket.timeout:
            r.append((ip, -1))
            continue
        Etime = time.time()
        delay = (Etime-Stime)*1000
        r.append((string, '%.3f' % (delay)))
    if len(r) == 1:
        return r[0]
    else:
        return r

