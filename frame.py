class segment:
    def __init__(self, id, frame, start, end, data):
        self.id = id
        self.frame = frame
        self.start = start
        self.end = end
        self.size = end - start
        self.data = data

    def __repr__(self):
        return str(self.__dict__)

    def send(self, socket):
        socket.send(self.data)

    def sendto(self, socket, addr):
        socket.sendto(self, data, addr)


class frame:
    def __init__(self):
        self.segs = []

    def __repr__(self):
        return str(self.__dict__)

    def size(self):
        return self.pkt_size

    def make_segs(self, data, step):
        end_pos = self.pkt_pos + self.pkt_size
        sid = 0
        for i in range(self.pkt_pos, end_pos, step):
            if i + step > end_pos:
                self.segs.append(
                    segment(sid, self, i, end_pos, data[i:end_pos]))
            else:
                self.segs.append(
                    segment(sid, self, i, i + step, data[i:i + step]))
            sid += 1

