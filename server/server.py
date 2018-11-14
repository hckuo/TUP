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


def onlyUsingUDP(vdata):
    s_udp = create_udp_socket()
    u_count = 0
    for bt in vdata:
        u_bytes.append(bt)
        u_count += 1
        if u_count == BYTE_STEP:
            send_udp_socket(s_udp, u_bytes)
            u_count = 0
            u_bytes = bytearray()
    send_udp_socket(s_udp, u_bytes)
    s_udp.close()


def onlyUsingTCP(vdata):
    s_tcp = create_tcp_socket()
    for i in range(len(vdata), step=BYTE_STEP):
        if i + BYTE_STEP > len(vdata):
            send_tcp_socket(s_tcp, vdata[i:])
        else:
            send_tcp_socket(s_tcp, vdata[i:i + BYTE_STEP])
    s_tcp.close()


## check input file byte by byte if it is in the given range
def buffer_frame(vdata, videoRange):
    s_udp = create_udp_socket()
    t_count = 0
    u_count = 0
    t_bytes = bytearray()
    u_bytes = bytearray()
    prevRange = 0
    fileLen = len(vdata)
    for currentRange in videoRange:
        for count in range(prevRange, currentRange[0]):
            u_bytes.append(vdata[count])
            u_count += 1
            if u_count == BYTE_STEP:
                send_udp_socket(s_udp, u_bytes)
                u_count = 0
                u_bytes = bytearray()
        send_udp_socket(s_udp, u_bytes)
        u_count = 0
        u_bytes = bytearray()
        for count in range(currentRange[0], currentRange[1]):
            t_bytes.append(vdata[count])
            t_count += 1
            count += 1
            if t_count == BYTE_STEP:
                tcp_sender(t_bytes)
                t_count = 0
                t_bytes = bytearray()
        tcp_sender(t_bytes)
        prevRange = currentRange[1]
    for count in range(prevRange, fileLen):
        u_bytes.append(vdata[count])
        u_count += 1
        if u_count == BYTE_STEP:
            send_udp_socket(s_udp, u_bytes)
            u_count = 0
            u_bytes = bytearray()
    send_udp_socket(s_udp, u_bytes)
    s_udp.close()


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
    #  buffer_frame(vdata, IRange)
    tend = datetime.now()
    print('TUP(our method) time used:')
    print(tend - tstart)

    tstart = datetime.now()
    onlyUsingTCP(vdata)
    tend = datetime.now()
    print('TCP time used:')
    print(tend - tstart)

    tstart = datetime.now()
    onlyUsingUDP(vdata)
    tend = datetime.now()
    print('UDP time used:')
    print(tend - tstart)
