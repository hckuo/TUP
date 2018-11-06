import sys
sys.path.insert(0, '../lib')
from pic import *
from sender import *

## check input file byte by byte if it is in the given range
def buffer_frame(fileName, videoRange):

    s_udp = create_udp_socket()

    cc = 0
    count = 0
    with open(fileName, 'rb') as f:
        while (1):
            x0 = f.read(1) #read byte by byte
            if not x0:
                break
            xhex = binascii.hexlify(x0)
            flag = False
            
            currentRange = videoRange[0]
            for r in videoRange:
                if count>=r[0] and count < r[1]:
                    flag = True
                    currentRange=r
                    break
                if count<r[0]:
                    break
            if flag:
                my_bytes = bytearray()
                for i in range(currentRange[0], currentRange[1]):
                    my_bytes.append(ord(x0))
                    x0 = f.read(1)
                    count+=1
                s_tcp = create_tcp_socket()
                send_tcp_socket(s_tcp,my_bytes)
                s_tcp.close()

            else:
                #element OUT of the range will go here
                send_udp_socket(s_udp,x0)
                count += 1
    s_udp.close()
    

##TESTING FUNCTION
if __name__ == '__main__':
    fileName = 'small.mp4'
    metaName = 'new.txt'
    
    fs = getFrames(metaName)
    IRange = getIRange(fs)
    PRange = getPRange(fs)
    print (IRange)

    buffer_frame(fileName, IRange)

