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


## check input file byte by byte if it is in the given range
def buffer_frame(fileName, videoRange):
    count = 0
    with open(fileName, 'rb') as f:
        while (1):
            x0 = f.read(1)
            if not x0:
                break
            xhex = binascii.hexlify(x0)
            count += 1
            flag = False
            for r in videoRange:
                if r[0] <= count and count < r[1]:
                    flag = True
            if flag:
                #element IN the range will go here
                print("TCP", end=' ')
            else:
                #element OUT of the range will go here
                print("UDP", end=' ')


##TESTING FUNCTION
if __name__ == '__main__':
    fileName = '../input.mp4'
    metaName = '../frame.txt'
    fs = getFrames(metaName)
