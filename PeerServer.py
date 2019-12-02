from threading import Thread
import socket
import json

class PeerServer():

    def __init__(self, host, port, dvr):

        self.dvr = dvr

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.thread = Thread(target=self.handle_incoming_connection, args=(host, port))
        self.thread.start()

    def handle_incoming_connection(self, host, port):

        # wait for everything to initialize
        while not self.dvr.server_running:
            pass

        get_key = lambda d, v: next(k for k, l in d.items() if l == v)
        me = get_key(self.dvr.servers, (host, port))

        dvr = self.dvr
        sock = self.socket

        while True:
            data, addr = sock.recvfrom(4096)

            dvr.packets += 1
            vect = json.loads(data.decode('utf-8'))
            src = get_key(dvr.servers, addr)


            for k,v in dvr.node_table[me]:





