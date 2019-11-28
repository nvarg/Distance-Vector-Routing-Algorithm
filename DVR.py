import math
from threading import Thread

from InputController import InputController
from TimedFunc import TimedFunc
from PeerServer import PeerServer
from Peer import Peer

class DVR():

    def __init__(self):
        self.server_running = False
        self.myid = None
        self.neighbors = None
        self.node_table = None

        InputController(self)

    def __del__(self):
        self.crash()

    def server(self, _t, filename, _i, update_interval):
        '''Reads the topology file, initiates the node table, and starts the update & server thread'''
        self.server_running = True

        with open(filename, 'r') as f:
            num_servers = int(f.readline())
            num_neighbors = int(f.readline())

            servers = dict.fromkeys(range(1, num_servers+1))
            neighbors = dict()

            for i in range(0, num_servers):
                line = f.readline()
                id, ip, port = (int(i) if '.' not in i else i for i in line.split())
                servers[id] = ip, port

            for i in range(0, num_neighbors):
                line = f.readline()
                self.myid, neighbor, cost = (int(i) for i in line.split())
                neighbors[neighbor] = cost

        me = servers[self.myid]

        dzip = lambda k, v: dict(zip(k, v))
        initiate_table = lambda: dzip(range(1, num_servers+1), [math.inf]*(num_servers+1))

        PeerServer(*me)

        self.node_table = {id: initiate_table() for id in range(1, num_servers+1)}
        self.neighbors = {id: Peer(addrs=servers[id]) for id in neighbors.keys()}

        # Establish links and create a neighbor connection table {'<id>': <sock object>...}
        # Create a node table with link costs
        TimedFunc(self.step, float(update_interval))

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
        server = int(server)
        print(f'{self.neighbors.keys()=}, {server} {type(server)}')
        if server not in self.neighbors.keys():
            print(f'disable: server number {server} is not in neighbor list')
            return
        self.neighbors[server].sock.close()
        del self.neighbors[server];
        self.node_table[self.myid][server] = math.inf
        print('disable: SUCCESS')

    def crash(self):
        '''Closes all server connections. The neighboring servers must
        handle this close correctly and set the link cost to infinity.'''
        for id, p in self.neighbors.items():
            disable(self, id)
        print('Crash: SUCCESS')


if __name__ == "__main__":
    DVR()
