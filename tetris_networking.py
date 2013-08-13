import socket
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 3715

def main():
    import sys
    print(sys.argv)
    import tetris

if __name__ == "__main__":
    main()

def encode_blocks(self, blocks):
    msg += "blocks:"
    for block in blocks:
        msg += str(block.x) + "," + str(block.y) + ";"
    return msg

def decode_blocks(self):
    msgtype, msg = rcvd.split(":")
    if msgtype == "blocks":
        coords = msgtype.strip(";").split(";")
        blocks = []
        for coord in coords:
            x,y = coord.split(",")
            blocks.append(Block(x, y, pygame.Color("grey")))
    return blocks

class Server(threading.Thread):
    def __init__(self, logic):
        Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        self.logic = logic
        self.lock = threading.Lock()

    def run(self):
        data, addr = sock.recvfrom(1024)

        while data != "disconnect":
            blocks = decode_blocks(data)

class Client(threading.Thread):
    def __init__(self, logic):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        self.logic = logic
        self.lock = threading.Lock()

class Peer(threading.Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.msg = ""
        self.rcvd = ""

    def start_server(self, udp_port = UDP_PORT):
        sock.bind((UDP_IP, udp_port))
        data, addr = self.sock.recvfrom(buf_size)
        self.start()

    def run(self):
        pass

    def encode_shape(self, shape):
        pass

    
    def send(self, blocks):
        encoded = self.encode_blocks(blocks)
        sock.sendto(self.msg, (UDP_IP, UDP_PORT))


