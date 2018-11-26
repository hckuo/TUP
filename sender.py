import sys
from datetime import datetime
from socket import *
from pic import *
import argparse

host = 'localhost'
byte_step = 1024
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--udp', action='store_true')
parser.add_argument('--host')
parser.add_argument('-s', '--step')
args = parser.parse_args()
if args.host:
    host = args.host
if args.step:
    byte_step = args.step

def create_tcp_socket():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, 6677))
    s.listen(5)
    return s


def create_udp_socket():
    s = socket(AF_INET, SOCK_DGRAM)
    return s


def send_with_connection(conn, data, step=byte_step):
    for i in range(0, len(data), step):
        if i + step > len(data):
            conn.send(data[i:])
        else:
            conn.send(data[i:i+step])
    conn.close()

def sendto_with_socket(s, data, addr=(host, 8888), step=byte_step):
    for i in range(0, len(data), step):
        if i + step > len(data):
            s.sendto(data[i:], addr)
        else:
            s.sendto(data[i:i+step], addr)
    s.sendto(b'', addr)

def get_bytes_from_file(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data


def send_UDP(vdata):
    s = create_udp_socket()
    tstart = datetime.now()
    sendto_with_socket(s, vdata)
    tend = datetime.now()
    print('UDP time used:')
    print(tend - tstart)
    s.close()


def send_TCP(vdata):
    s = create_tcp_socket()
    conn, addr = s.accept()
    tstart = datetime.now()
    send_with_connection(conn, vdata)
    tend = datetime.now()
    print('TCP time used:', end='')
    print(tend - tstart)
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

    #  fileName = 'videos/rabbit.mp4'
    fileName = 'videos/uiuc.mp4'
    metaName = fileName + '.meta'

    vdata = get_bytes_from_file(fileName)

    fs = getFrames(metaName)
    IRange = getIRange(fs)
    PRange = getPRange(fs)

    #  tstart = datetime.now()
    #  send_TUP(vdata, IRange)
    #  tend = datetime.now()
    #  print('TUP(our method) time used:')
    #  print(tend - tstart)

    if args.udp:
        print('Sending UDP')
        send_UDP(vdata)
    else:
        print('Sending TCP')
        send_TCP(vdata)

