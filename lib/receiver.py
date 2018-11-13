from socket import *
from select import select

def read_tcp(s):
    client,addr = s.accept()
    data = client.recv(2048)
    client.close()
    #print ("Recv TCP:' %s '" % data)

def read_udp(s):
    data, addr = s.recvfrom(2048)
    #print ("Recv UDP:' %s '" % data)

def run():
    host = '127.0.0.1'
    port1 = 6677 #port for TCP 
    port2 = 8888 #port for UDP
    backlog = 5

    # create tcp socket
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.bind((host,port1))
    tcp.listen(backlog)

    # create udp socket
    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind((host,port2))

    input = [tcp,udp]
    while True:
        inputready,outputready,exceptready = select(input,[],[])
        for s in inputready:
            if s == tcp:
                read_tcp(s)
            elif s == udp:
                read_udp(s)
            else:
                print ("unknown socket:", s)

    

## TESTING FUNCTION
if __name__ == '__main__':
    fileName = '../server/small.mp4'
    metaName = '../server/new.txt'
    run()
