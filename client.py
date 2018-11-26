from socket import *
from select import select

byte_step = 1024
host = 'localhost'
tcp_port = 6677

def read_tcp(s):
    return data


def read_udp(s):
    data, addr = s.recvfrom(byte_step)
    return data


def receive():
    data = bytearray()
    port2 = 8888  #port for UDP
    backlog = 5

    # create tcp socket
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect((host, port1))

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
    s.connect((host, tcp_port))
    while True:
        chunk = s.recv(byte_step)
        data += chunk
        if chunk == b'':
            s.close()
            print('close conn')
            break;
    return data



## TESTING FUNCTION
if __name__ == '__main__':
    fileName = 'videos/uiuc.mp4'
    metaName = fileName + '.meta'
    data = receive_tcp()
    with open('output.mp4', 'wb') as f:
        f.write(data)

