import socket
import sys

class Peer():

    def __init__(self, sock, address=None):

        self.sock= sock

        self.thread = Thread(target=self.handle_incoming_packet, args=(,))
        self.thread.start()

    def handle_incoming_packet(self):
        while True:
            packet = self.sock.recv(4096)

            if len(packet) == 0:
                break # indicates that the connection timed-out or is otherwise lost

            # Handle packet here

        sys.exit()
