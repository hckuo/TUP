class segment:
    def __init__(self, id, frameid, start, end)
        self.id = id
        self.frameid = frameid
        self.start = start
        self.end = end
        self.size = end - start

class frame:
    def __init__(self, type, id, start, end)
        self.type = type
        self.id = id
        self.start = start
        self.end = end
        self.size = end - start
        self.segs = []

    def segments(self, step=1024):
        sid = 0
        for i in range(self.start, self.end, step):
            if i + step > end:
                self.segs.append(segment(sid, self.id, i, end))
            else:
                self.segs.append(segment(sid, self.id, i, i+step))
            sid += 1



