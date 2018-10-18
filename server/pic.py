import subprocess
import os
import binascii

## use ffprobe -show_frames input.mp4 to get video meta data

## return array of frame (not used)
def getIDtype(fileName):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [fileName]).decode()
    frame_types = out.replace('pict_type=','').split()
    return zip(range(len(frame_types)), frame_types)

## save raw data of specific frame (not used)
def getRawByte(fileName, index):
    FNULL = open(os.devnull, 'w')
    command = 'ffmpeg -i ' + str(fileName) + ' -c:v libx264 -filter:v "select=gte(n\,'+str(index)+')" -frames:v 1 -f h264 frame'+str(index)+'.h264'
    subprocess.call(command,shell=True, stderr=subprocess.DEVNULL)

## get the range array of media_type = video
def getVidRange(metaName):
    vidList = []
    with open(metaName,'r') as f:
        content = f.readlines()
    for lineNum in range(len(content)):
        #print(line)
        if content[lineNum] == 'media_type=video\n':
            start_pkt = (int)(content[lineNum+10].split("=")[1])
            range_pkt = (int)(content[lineNum+11].split("=")[1])
            p = [start_pkt+1,start_pkt+range_pkt+1] #[0, 10)
            vidList.append(p)
    return vidList

## get the range array of keyframe (I type)         
def getIRange(metaName):
    vidList = []
    with open(metaName,'r') as f:
        content = f.readlines()
    for lineNum in range(len(content)):
        #print(line)
        if content[lineNum] == 'media_type=video\n':
            if content[lineNum+1] == 'key_frame=1\n':
                start_pkt = (int)(content[lineNum+10].split("=")[1])
                range_pkt = (int)(content[lineNum+11].split("=")[1])
                p = [start_pkt+1,start_pkt+range_pkt+1] #[0, 10)
                vidList.append(p)
    return vidList

## get the range array of non keyframe (P type)
def getPRange(metaName):
    vidList = []
    with open(metaName,'r') as f:
        content = f.readlines()
    for lineNum in range(len(content)):
        #print(line)
        if content[lineNum] == 'media_type=video\n':
            if content[lineNum+1] == 'key_frame=0\n':
                start_pkt = (int)(content[lineNum+10].split("=")[1])
                range_pkt = (int)(content[lineNum+11].split("=")[1])
                p = [start_pkt+1,start_pkt+range_pkt+1] #[0, 10)
                vidList.append(p)
    return vidList

## check input file byte by byte if it is in the given range 
def buffer_frame(fileName, videoRange):
    count = 0
    with open(fileName, 'rb') as f:
        while(1):
            x0 = f.read(1)
            if not x0:
                break
            xhex =binascii.hexlify(x0)
            count+=1
            flag = False
            for r in videoRange:
                if r[0]<= count and count < r[1]:
                    flag = True
            if flag:
                #element IN the range will go here
                print("TCP", end=' ')
            else:
                #element OUT of the range will go here
                print("UDP", end=' ')

##TESTING FUNCTION
if __name__ == '__main__':
    fileName = "/home/hsinyuh2/project/input.mp4"
    metaName = '/home/hsinyuh2/project/frame.txt'
    i = getIRange(metaName)
    print (i)
    buffer_frame(fileName, i)
