import json
import math
import asyncio
import socket
import sys

class DVR_Protocol():

    def __init__(self):
        pass

    async def run(self):
        '''Initiates the async input loop'''
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        self.loop.create_task(await self.handle_input())

    def parse_command(self, msg):
        args = msg.split()
        try:
            command = getattr(self, args[0])
        except:
            print(f'Invalid command: "{args[0]}" with args: {args[1:]}')
            command = lambda *args: args # do nothing
        command(*args[1:])

    async def handle_input(self):
        '''Waits for stdin then passes to control to a command parser'''

        while True:
            line = await self.loop.run_in_executor(None, sys.stdin.readline)
            self.parse_command(line)

    async def handle_incoming_connection(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            local_endpoint = (host, port)
            sock.setblocking(False)
            sock.bind(local_endpoint)
            sock.listen(1)
            while True:
                conn, address = await self.loop.sock_accept(sock)
                incoming_ip, incoming_port = address

                # Handle incoming connection
                print(f'incoming connection from {incoming_ip}:{incoming_port}')

    async def handle_incoming_packet(self, connection):
        while True:
            packet = await self.loop.sock_recv(connection)

            if len(packet) == 0:
                break # indicates that the connection timed-out or is otherwise lost

            # Handle packet here

    async def periodic_update(self, delay):
        while True:
            await asyncio.sleep(delay)
            self.step()

    def server(self, _t, filename, _i, update_interval):
        print(f'{filename=}')
        with open(filename, 'r') as f:
            num_servers = int(f.readline())
            num_neighbors = int(f.readline())

            servers = dict.fromkeys(range(1, num_servers+1))
            neighbors = [math.inf for i in range(0, num_neighbors)]

            print(f'{servers=}')
            print(f'{neighbors=}')

            for i in range(0, num_servers):
                line = f.readline()
                id, ip, port = (int(i) if '.' not in i else i for i in line.split())
                servers[id] = ip, port

            for i in range(0, num_neighbors):
                line = f.readline()
                server, neighbor, cost = (int(i) for i in line.split())
                neighbors[neighbor] = cost

            # Establish links and create a neighbor connection table {'<id>': <sock object>...}
            # Create a node table with link costs

    def update(self, server1, server2, cost):
        if cost == 'inf':
            cost = math.inf
        pass

    def step(self):
        # update node table here
        pass

    def packets(self):
        '''Display the number of distance vector (packets) this  server
        has  received  since  the  last  invocation of this information'''
        pass

    def display(self):
        '''Display the current routing table formatted as a sequence
        of lines, with each line indicating: <source-server-ID> <next-hop-server-ID> <cost-of-path>'''
        pass

    def disable(self, server):
        '''Closes the connection with the given server id'''
        pass

    def crash(self):
        '''Closes all server connections. The neighboring servers must
        handle this close correctly and set the link cost to infinity.'''
        pass


if __name__ == "__main__":
    asyncio.run(DVR_Protocol().run())

