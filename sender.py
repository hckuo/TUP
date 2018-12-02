import argparse
from datetime import datetime
from frame import frame
from operator import attrgetter
from socket import socket, AF_INET, SOCK_STREAM,SO_REUSEADDR, SOL_SOCKET, SOCK_DGRAM
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--udp', action='store_true')
parser.add_argument('-t', '--tcp', action='store_true')
parser.add_argument('--host', default='localhost')
parser.add_argument('-s', '--step',type=int,default=1024)
parser.add_argument('-v', '--video', default='videos/uiuc.mp4')
args = parser.parse_args()

def create_tcp_socket():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((args.host, 16677))
    s.listen(5)
    return s


def create_udp_socket():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return s


def send_with_connection(conn, data, step=args.step):
    for i in range(0, len(data), step):
        if i + step > len(data):
            conn.send(data[i:])
        else:
            conn.send(data[i:i+step])
    conn.close()

def sendto_with_socket(s, data, addr=(args.host, 18888), step=args.step):
    for i in range(0, len(data), step):
        if i + step > len(data):
            s.sendto(data[i:], addr)
        else:
            s.sendto(data[i:i+step], addr)
    s.sendto(b'', addr)


def send_UDP(frames):
    sock = create_udp_socket()
    tstart = datetime.now()
    for f in frames:
        for s in f.segs:
            sock.sendto(s.udp_meta + s.data, (args.host, 18888))
    sock.sendto(b'', (args.host, 18888))
    tend = datetime.now()
    print('UDP time used:')
    print(tend - tstart)
    sock.close()


def send_TCP(frames):
    sock = create_tcp_socket()
    conn, addr = sock.accept()
    tstart = datetime.now()
    for f in frames:
        for s in f.segs:
            conn.send(s.data)
    tend = datetime.now()
    print('TCP time used:', end='')
    print(tend - tstart)
    sock.close()

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


def getFrames(videoPath):
    frames = []
    for line in open(videoPath+'.meta'):
        if line == '[FRAME]\n':
            f = frame()
        elif line == '[/FRAME]\n':
            frames.append(f)
            f = None
        else:
            var = line.strip().split('=')[0]
            value = line.strip().split('=')[1]
            if value.isdigit():
                value = int(value)
            setattr(f, var, value)

    with open(videoPath, 'rb') as f:
        data = f.read()
        f.close()

    frames.sort(key=attrgetter('pkt_pos'))
    headerframe = frame()
    setattr(headerframe, 'pkt_pos', 0)
    setattr(headerframe, 'pkt_size', frames[0].pkt_pos)
    frames.insert(0, headerframe)
    tailframe = frame()
    setattr(tailframe, 'pkt_pos', frames[-1].pkt_pos + frames[-1].pkt_size)
    setattr(tailframe, 'pkt_size', len(data) - tailframe.pkt_pos)
    frames.append(tailframe)

    for f in frames:
        f.make_segs(data, args.step)

    return frames

if __name__ == '__main__':

    frames = getFrames(args.video)

    #  tstart = datetime.now()
    #  send_TUP(vdata, IRange)
    #  tend = datetime.now()
    #  print('TUP(our method) time used:')
    #  print(tend - tstart)

    if args.udp:
        print('Sending UDP')
        send_UDP(frames)
    if args.tcp:
        print('Sending TCP')
        send_TCP(frames)

