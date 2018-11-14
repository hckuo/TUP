import sys
from datetime import datetime
sys.path.insert(0, '../lib')
from sender import *
from pic import *

def get_bytes_from_file(filename):  
    return open(filename, "rb").read()

def onlyUsingUDP(fileName):
    s_udp = create_udp_socket()
    u_bytes = bytearray()
    u_count = 0
    fileArray = get_bytes_from_file(fileName)
    for bt in fileArray:
        u_bytes.append(bt)
        u_count += 1
        if u_count==2048:
            send_udp_socket(s_udp,u_bytes)
            u_count=0
            u_bytes = bytearray()
    send_udp_socket(s_udp,u_bytes)
    s_udp.close()

def onlyUsingTCP(fileName):
    t_bytes = bytearray()
    t_count = 0
    fileArray = get_bytes_from_file(fileName)
    for bt in fileArray:
        t_bytes.append(bt)
        t_count += 1
        if t_count==2048:
            s_tcp = create_tcp_socket()
            send_tcp_socket(s_tcp,t_bytes)
            s_tcp.shutdown(SHUT_WR)
            s_tcp.close()
            t_count=0
            t_bytes = bytearray()
    s_tcp = create_tcp_socket()
    send_tcp_socket(s_tcp,t_bytes)
    s_tcp.close()        

## check input file byte by byte if it is in the given range
def buffer_frame(fileName, videoRange):
    s_udp = create_udp_socket()
    t_count = 0
    u_count = 0
    t_bytes = bytearray()
    u_bytes = bytearray()
    prevRange = 0
    fileArray = get_bytes_from_file(fileName)
    fileLen = len(fileArray)
    for currentRange in videoRange:
        for count in range(prevRange, currentRange[0]):
            u_bytes.append(fileArray[count])
            u_count += 1
            if u_count==2048:
                send_udp_socket(s_udp,u_bytes)
                u_count=0
                u_bytes = bytearray()
        send_udp_socket(s_udp,u_bytes)
        u_count=0
        u_bytes = bytearray()
        for count in range(currentRange[0], currentRange[1]):
            t_bytes.append(fileArray[count])
            t_count += 1
            count += 1
            if t_count==2048:
                tcp_sender(t_bytes)
                t_count=0
                t_bytes = bytearray()
        tcp_sender(t_bytes)
        prevRange = currentRange[1]
    for count in range(prevRange, fileLen):
        u_bytes.append(fileArray[count])
        u_count += 1
        if u_count==2048:
            send_udp_socket(s_udp,u_bytes)
            u_count=0
            u_bytes = bytearray()
    send_udp_socket(s_udp,u_bytes)
    s_udp.close()
def tcp_sender(btArray):
    s_tcp = create_tcp_socket()
    send_tcp_socket(s_tcp,btArray)
    s_tcp.shutdown(SHUT_WR)
    s_tcp.close()

##TESTING FUNCTION
if __name__ == '__main__':
    fileName = 'small.mp4'
    metaName = 'new.txt'
    #fileName = '../input.mp4'
    #metaName = '../frame.txt'
    
    fs = getFrames(metaName)
    IRange = getIRange(fs)
    PRange = getPRange(fs)
    print (IRange)
    
    tstart = datetime.now()
    buffer_frame(fileName, IRange)
    tend = datetime.now()
    print('TUP(our method) time used:')
    print(tend-tstart)

    tstart = datetime.now()
    onlyUsingTCP(fileName)
    tend = datetime.now()
    print('TCP time used:')
    print(tend-tstart)

    tstart = datetime.now()
    onlyUsingUDP(fileName)
    tend = datetime.now()
    print('UDP time used:')
    print(tend-tstart)

