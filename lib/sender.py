from socket import *
import random


def create_tcp_socket():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('localhost', 6677))
    s.listen()
    return s


def create_udp_socket():
    s = socket(AF_INET, SOCK_DGRAM)
    return s


def send_with_connection(conn, data, step=2048):
    for i in range(0, len(data), step):
        if i + step > len(data):
            conn.send(data[i:])
        else:
            conn.send(data[i:i+step])
    conn.close()

def sendto_with_socket(s, data, addr=('localhost', 8888), step=2048):
    for i in range(0, len(data), step):
        if i + step > len(data):
            s.sendto(data[i:], addr)
        else:
            s.sendto(data[i:i+step], addr)

