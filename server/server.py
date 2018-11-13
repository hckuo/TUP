import sys
from datetime import datetime
sys.path.insert(0, '../lib')
from pic import *
from sender import *

def onlyUsingUDP(fileName):

    s_udp = create_udp_socket()
    u_bytes = bytearray()
    u_count = 0
    with open(fileName, 'rb') as f:
        while (1):
            x0 = f.read(1) #read byte by byte
            if not x0:
                send_udp_socket(s_udp,u_bytes)
                s_udp.close()
                break
            u_bytes.append(ord(x0))
            u_count += 1
            if u_count==2048:
                send_udp_socket(s_udp,u_bytes)
                u_count=0
                u_bytes = bytearray()

def onlyUsingTCP(fileName):
    t_bytes = bytearray()
    t_count = 0
    with open(fileName, 'rb') as f:
        while (1):
            x0 = f.read(1) #read byte by byte
            if not x0:
                s_tcp = create_tcp_socket()
                send_tcp_socket(s_tcp,t_bytes)
                s_tcp.close()
                break
            t_bytes.append(ord(x0))
            t_count += 1
            if t_count==2048:
                s_tcp = create_tcp_socket()
                send_tcp_socket(s_tcp,t_bytes)
                s_tcp.shutdown(SHUT_WR)
                s_tcp.close()
                t_count=0
                t_bytes = bytearray()
            

## check input file byte by byte if it is in the given range
def buffer_frame(fileName, videoRange):

    s_udp = create_udp_socket()

    cc = 0
    t_count = 0
    u_count = 0
    count= 0
    t_bytes = bytearray()
    u_bytes = bytearray()
    nextTCP = 0
    rangeLen = len(videoRange)
    currentRange = videoRange[0]
    with open(fileName, 'rb') as f:
        while (1):
            x0 = f.read(1) #read byte by byte
            if not x0:
                send_udp_socket(s_udp,u_bytes)
                s_udp.close()
                break
            xhex = binascii.hexlify(x0)
            flag = False
            
            if nextTCP<rangeLen and count>=videoRange[nextTCP][0] and count < videoRange[nextTCP][1]:
                flag = True
                currentRange=videoRange[nextTCP]
            
            if flag:
                #print("TR")
                send_udp_socket(s_udp,u_bytes)
                u_count=0
                u_bytes = bytearray() 
                for i in range(currentRange[0], currentRange[1]):
                    t_bytes.append(ord(x0))
                    x0 = f.read(1)
                    t_count += 1
                    count += 1
                    if t_count==2048 or i==(currentRange[1]-1):
                        s_tcp = create_tcp_socket()
                        send_tcp_socket(s_tcp,t_bytes)
                        s_tcp.shutdown(SHUT_WR)
                        s_tcp.close()
                        t_count=0
                        t_bytes = bytearray()
                nextTCP+=1
            else:
                #element OUT of the range will go here
                u_bytes.append(ord(x0))
                u_count += 1
            if u_count==2048:
                send_udp_socket(s_udp,u_bytes)
                u_count=0
                u_bytes = bytearray()
            count+=1
    s_udp.close()
    

##TESTING FUNCTION
if __name__ == '__main__':
    #fileName = 'small.mp4'
    #metaName = 'new.txt'
    fileName = '../input.mp4'
    metaName = '../frame.txt'
    
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

