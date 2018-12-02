from socket import *
from select import select
import collections
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--udp', action='store_true')
parser.add_argument('-t', '--tcp', action='store_true')
parser.add_argument('--host', default='localhost')
parser.add_argument('-s', '--step', type=int, default=1024)
args = parser.parse_args()
tcp_port = 16677
udp_port = 18888


def read_tcp(s):
    return data


def read_udp(s):
    data, addr = s.recvfrom(args.step)
    return data


def receive():
    data = bytearray()
    port2 = 8888  #port for UDP
    backlog = 5

    # create tcp socket
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect((args.host, port1))

    # create udp socket
    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind(("", port2))

    sockets = [tcp, udp]
    while True:
        inputready, outputready, exceptready = select(sockets, [], [])
        for s in inputready:
            if s == tcp:
                data += read_tcp(s)
            elif s == udp:
                data += read_udp(s)
            else:
                print("unknown socket:", s)
    tcp.close()
    udp.close()
    return data


def receive_tcp():
    data = bytearray()
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((args.host, tcp_port))
    while True:
        chunk = s.recv(args.step)
        data += chunk
        if chunk == b'':
            s.close()
            print('close conn')
            break
    return data


def receive_udp():
    data = bytearray()
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((args.host, udp_port))
    data_dict = {}
    while True:
        header, addr = s.recvfrom(32)
        f_pos = int.from_bytes(header[0:7], 'little')
        f_size = int.from_bytes(header[8:15], 'little')
        s_pos = int.from_bytes(header[16:23], 'little')
        s_size = int.from_bytes(header[24:31], 'little')
        chunk, addr = s.recvfrom(s_size)
        data_dict[s_pos] = chunk

        if chunk == b'':
            print('UDP end recv')
            s.close()
            break

    prev = 0
    for pos, chunk in sorted(data_dict.items()):
        if pos == prev:
            data += chunk
        else:
            data += b'0x0' * (pos - prev)
        prev = len(data)

    return data


if __name__ == '__main__':
    if args.udp:
        print('reciving UDP')
        data = receive_udp()
    if args.tcp:
        print('reciving TCP')
        data = receive_tcp()
    with open('output.mp4', 'wb') as f:
        f.write(data)
