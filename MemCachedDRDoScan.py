#!/usr/bin/env python
import socket
import select
import requests
import gevent
from gevent import monkey, pool
import sys
import getopt
monkey.patch_all()
jobs = []



def MemcacheCheck(ip):
    timeout=3
    addr=(ip,11211)
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    data="\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
    s.sendto(data,addr)
    s.setblocking(0)
    data=""
    ready = select.select([s], [], [], timeout)
    try:
        data,addr2=s.recvfrom(2048)
    except:
        pass
    if len(data)>15:
        print ip
    s.close()

#MemcacheCheck("120.194.198.14")


def main(argv):
    MaxProcs=1000
    if len(argv)==0:
        print sys.argv[0]+' -i ipaddress.txt [-P max-procs]'
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv,"hi:t:")
    except getopt.GetoptError:
        print sys.argv[0]+' -i ipaddress.txt [-P max-procs]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0]+' -i ipaddress.txt [-P max-procs]'
            sys.exit()
        elif opt in ("-P"):
            MaxProcs = int(arg)
        elif opt in ("-i"):
            ipadd = arg

    p = pool.Pool(MaxProcs)
    with open(ipadd, 'r') as fp:
        for line in fp:
            jobs.append(p.spawn(MemcacheCheck, line.strip("\n")))
        gevent.joinall(jobs)

if __name__ == '__main__':
    main(sys.argv[1:])