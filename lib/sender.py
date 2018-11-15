from socket import *
import random


def create_tcp_socket():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 6677))
    return s


def create_udp_socket():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('localhost', 8888))
    return s


def send_with_socket(s, data, step=2048):
    for i in range(0, len(data), step):
        if i + step > len(data):
            s.send(data[i:])
        else:
            s.send(data[i:i+step])

def sendto_with_socket(s, data, addr=('localhost', 8888), step=2048):
    for i in range(0, len(data), step):
        if i + step > len(data):
            s.sendto(data[i:], addr)
        else:
            s.sendto(data[i:i+step], addr)


### COMBINE TESTING METHOD ###
def send_tcp():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 6677))
    data = 'Hello TCP'
    s.send(data)
    s.close()


### COMBINE TESTING METHOD ###
def send_udp():
    s = socket(AF_INET, SOCK_DGRAM)
    data = 'Hello UDP'
    s.sendto(data, ('localhost', 8888))
    s.close()


## TESTING FUNCTION
if __name__ == '__main__':
    s_udp = create_udp_socket()
    i = 0
    while i < 150:
        r = random.randint(1, 2)
        if r == 1:
            send_udp_socket(s_udp, str(i))
        else:
            s_tcp = create_tcp_socket()
            send_tcp_socket(s_tcp, str(i))
            #s_tcp.close()
        i = i + 1

    s_udp.close()
    s_tcp.close()
