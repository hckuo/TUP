import binascii
import os
import subprocess


class Frame:
    def __init__(self):
        pass

    def isVideoFrame(self):
        return self.media_type == 'video'

    def isIFrame(self):
        return self.key_frame == '1'

    def isPFrame(self):
        return self.key_frame == '0'

    def get(self, var):
        return getattr(self, var)


## use "ffprobe -show_frames input.mp4 > frame.txt" to get video meta data


## return array of frame (not used)
def getIDtype(fileName):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split(
    )
    out = subprocess.check_output(command + [fileName]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types) 

## save raw data of specific frame (not used)
def getRawByte(fileName, index):
    FNULL = open(os.devnull, 'w')
    command = 'ffmpeg -i ' + str(
        fileName) + ' -c:v libx264 -filter:v "select=gte(n\,' + str(
            index) + ')" -frames:v 1 -f h264 frame' + str(index) + '.h264'
    subprocess.call(command, shell=True, stderr=subprocess.DEVNULL)


def getFrames(metaName):
    frames = []
    with open(metaName, 'r') as f:
        content = f.readlines()
        for line in content:
            if line == '[FRAME]\n':
                f = Frame()
            elif line == '[/FRAME]\n':
                frames.append(f)
                f = None
            else:
                var = line.strip().split('=')[0]
                value = line.strip().split('=')[1]
                setattr(f, var, value)
    return frames


## return the range of the video that is I frame type
def getIRange(fs):
    vidList = []
    for f in fs:
        if f.isVideoFrame() and f.isIFrame():
            start_pkt = int(f.pkt_pos)
            range_pkt = int(f.pkt_size)
            p = (start_pkt, start_pkt + range_pkt)  #[0, 10)
            vidList.append(p)
    return vidList


## return the range of the video that is P frame type
def getPRange(fs):
    vidList = []
    for f in fs:
        if f.isVideoFrame() and f.isPFrame():
            start_pkt = int(f.pkt_pos)
            range_pkt = int(f.pkt_size)
            p = [start_pkt, start_pkt + range_pkt]  #[0, 10)
            vidList.append(p)
    return vidList


##TESTING FUNCTION
if __name__ == '__main__':
    #fileName = '../input.mp4'
    fileName = '../server/small.mp4'
    #metaName = '../frame.txt'
    metaName = '../server/new.txt'

    #fs = getFrames(metaName)
    #IRange = getIRange(fs)
    #PRange = getPRange(fs)
    #print (IRange)
    #buffer_frame(fileName, IRange)
