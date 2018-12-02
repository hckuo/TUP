class segment:
    def __init__(self, id, frame, pos, end, data):
        self.id = id
        self.frame = frame
        self.pos = pos
        self.size = end - pos
        self.data = data
        self.udp_meta = b''
        self.udp_meta += (self.frame.pkt_pos).to_bytes(8, byteorder='little')
        self.udp_meta += (self.frame.pkt_size).to_bytes(8, byteorder='little')
        self.udp_meta += (self.pos).to_bytes(8, byteorder='little')
        self.udp_meta += (self.size).to_bytes(8, byteorder='little')

    def __repr__(self):
        return str(self.__dict__)

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
