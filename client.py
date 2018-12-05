from socket import *
from select import select
import collections
import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--udp', action='store_true')
parser.add_argument('-t', '--tcp', action='store_true')
parser.add_argument('-tu', '--tup', action='store_true')
parser.add_argument('--host', default='localhost')
parser.add_argument('-s', '--step', type=int, default=1024)
parser.add_argument('-o', '--output', default='output.mp4')
parser.add_argument('--giveup', action='store_true')
args = parser.parse_args()
tcp_port = 16677
udp_port = 18888


def receive_tup():

    data = bytearray()

    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind((args.host, udp_port))

    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect((args.host, tcp_port))

    sockets = [tcp, udp]
    tcprecv = 0
    udprecv = 0

    data_dict = {}
    tstart = datetime.now()
    missedcnt = 0
    expected = -1
    while sockets:
        readready, _, exceptready = select(sockets, [], sockets)

        for s in readready:
            if s == tcp:
                header = s.recv(32)
                if header == b'':
                    logger.info("TCP close")
                    s.close()
                    sockets.remove(s)
                    continue
                f_pos = int.from_bytes(header[0:8], 'little')
                f_size = int.from_bytes(header[8:16], 'little')
                s_pos = int.from_bytes(header[16:24], 'little')
                s_size = int.from_bytes(header[24:32], 'little')
                try:
                    chunk = s.recv(s_size)
                except MemoryError:
                    logger.warn(s_size)
                tcprecv += len(chunk)
            elif s == udp:
                payload, addr = s.recvfrom(1024 + 32)
                if payload == b'':
                    logger.info("UDP close")
                    if args.giveup:
                        tcp.send(b'\x00'*8)
                    s.close()
                    sockets.remove(s)
                    continue

                header = payload[:32]
                chunk = payload[32:]
                udprecv += len(chunk)
                f_pos = int.from_bytes(header[0:8], 'little')
                f_size = int.from_bytes(header[8:16], 'little')
                s_pos = int.from_bytes(header[16:24], 'little')
                s_size = int.from_bytes(header[24:32], 'little')
                if args.giveup:
                    if expected != -1 and expected != s_pos:
                        missedcnt += 1
                    if missedcnt == 1:
                        logger.debug("give up {}".format(f_pos))
                        tcp.send(header[:8])
                        missedcnt = 0
                    expected = s_pos + s_size
            else:
                assert(False)

            data_dict[s_pos] = chunk

    for pos, chunk in sorted(data_dict.items()):
        if len(data) < pos:
            logger.debug('data miss at {} size {}'.format(len(data), pos - len(data)))
            data += b'\x00' * (pos - len(data))
        data += chunk

    tend = datetime.now()
    print('recvsize tcp:{} udp:{} total:{} time:{}'.format(tcprecv, udprecv, tcprecv + udprecv, (tend-tstart).microseconds))

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
            logger.debug('close conn')
            break
    return data


def receive_udp():
    data = bytearray()
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((args.host, udp_port))
    data_dict = {}
    while True:
        payload, addr = s.recvfrom(1024 + 32)
        if payload == b'':
            logger.debug('UDP end recv')
            s.close()
            break
        header = payload[:32]
        chunk = payload[32:]
        f_pos = int.from_bytes(header[0:8], 'little')
        f_size = int.from_bytes(header[8:16], 'little')
        s_pos = int.from_bytes(header[16:24], 'little')
        s_size = int.from_bytes(header[24:32], 'little')
        data_dict[s_pos] = chunk

    for pos, chunk in sorted(data_dict.items()):
        if pos == len(data):
            data += chunk
        else:
            logger.debug('data miss at {} size {}'.format(len(data), pos - len(data)))
            data += b'\x00' * (pos - len(data))

    return data


if __name__ == '__main__':
    if args.udp:
        logger.debug('receiving UDP')
        data = receive_udp()
    if args.tcp:
        logger.debug('receiving TCP')
        data = receive_tcp()
    if args.tup:
        logger.debug('receiving TUP')
        data = receive_tup()
    with open(args.output, 'wb') as f:
        f.write(data)
