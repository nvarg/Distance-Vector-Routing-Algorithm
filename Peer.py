import socket
import sys

class Peer():

    def __init__(self, sock=None, addrs=None):
        assert not ((sock is not None) and (addrs is not None))
        assert not ((sock is None) and (addrs is None))

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(addrs)
        else:
            self.sock = sock

        self.thread = Thread(target=self.handle_incoming_packet)
        self.thread.start()

    def handle_incoming_packet(self):
        while True:
            packet = self.sock.recv(4096)

            if len(packet) == 0:
                break # indicates that the connection timed-out or is otherwise lost

            # Handle packet here
            print(f'{packet=}')

        sys.exit()
