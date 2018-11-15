import sys
from datetime import datetime
sys.path.insert(0, '../lib')
from sender import *
from pic import *

byte_step = 2048


def get_bytes_from_file(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data


def send_UDP(vdata):
    s = create_udp_socket()
    sendto_with_socket(s, vdata)
    s.close()


def send_TCP(vdata):
    s = create_tcp_socket()
    send_with_socket(s, vdata)
    s.close()


## check input file byte by byte if it is in the given range
def send_TUP(vdata, videoRange):
    tcp_data = bytearray()
    udp_data = bytearray()
    udp_start = 0
    for r in videoRange:
        tcp_start = r[0]
        udp_data += vdata[udp_start:tcp_start]
        udp_start = r[1]
        tcp_data += vdata[tcp_start:udp_start]
    udp_data += vdata[udp_start:]
    print(len(vdata))
    print(len(udp_data), len(tcp_data))
    #TODO: make sends concurrently
    send_TCP(tcp_data)
    send_UDP(udp_data)


def tcp_sender(btArray):
    s_tcp = create_tcp_socket()
    send_tcp_socket(s_tcp, btArray)
    s_tcp.shutdown(SHUT_WR)
    s_tcp.close()


##TESTING FUNCTION
if __name__ == '__main__':
    fileName = 'small.mp4'
    metaName = 'new.txt'
    #fileName = '../input.mp4'
    #metaName = '../frame.txt'

    vdata = get_bytes_from_file(fileName)

    fs = getFrames(metaName)
    IRange = getIRange(fs)
    PRange = getPRange(fs)
    print(IRange)

    tstart = datetime.now()
    send_TUP(vdata, IRange)
    tend = datetime.now()
    print('TUP(our method) time used:')
    print(tend - tstart)

    tstart = datetime.now()
    send_TCP(vdata)
    tend = datetime.now()
    print('TCP time used:')
    print(tend - tstart)

    tstart = datetime.now()
    send_UDP(vdata)
    tend = datetime.now()
    print('UDP time used:')
    print(tend - tstart)
