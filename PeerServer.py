from threading import Thread
import socket

class PeerServer():

    def __init__(self, host, port):
        self.thread = Thread(target=self.handle_incoming_connection, args=(host, port))
        self.thread.start()

    def handle_incoming_connection(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            sock.bind((host, port))
            sock.listen(1)
            while True:
                conn, address = sock.accept()
                incoming_ip, incoming_port = address

                # Handle incoming connection
                print(f'incoming connection from {incoming_ip}:{incoming_port}')

