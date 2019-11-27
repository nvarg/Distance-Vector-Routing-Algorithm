from threading import Thread
import socket

class PeerServer():

    def __init__(self, host, port):
        self.thread = Thread(target=self.handle_incoming_connection, args=(host, port))
        self.thread.start()

    def handle_incoming_connection(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(False)
            sock.bind((host, port))
            sock.listen(5)
            while True:
                conn, address = sock.accept()
                incoming_ip, incoming_port = address

                # Handle incoming connection
                print(f'Incoming connection from {incoming_ip}:{incoming_port}')
                Peer(sock=conn)

