import math

from InputController import InputController
from TimedFunc import TimedFunc
from PeerServer import PeerServer
from Peer import Peer

class DVR():

    def __init__(self):

        self.server_running = False
        self.myid = None
        self.node_table = None
        self.node_hops = None
        self.neighbors = None

        InputController(self)

    def __del__(self):
        self.crash()

    def server(self, _t, filename, _i, update_interval):
        '''Reads the topology file, initiates the node table, and starts the update & server thread'''
        if self.server_running:
            print('server: server was started, but it was already running.')
            return

        self.server_running = True

        with open(filename, 'r') as f:
            num_servers = int(f.readline())
            num_neighbors = int(f.readline())

            servers = dict.fromkeys([str(i) for i in range(1, num_servers+1)])
            neighbors = dict()

            for i in range(0, num_servers):
                line = f.readline()
                id, ip, port = line.split()
                servers[id] = ip, int(port)

            for i in range(0, num_neighbors):
                line = f.readline()
                self.myid, neighbor, cost = line.split()
                neighbors[neighbor] = int(cost)

        me = servers[self.myid]
        PeerServer(*me)

        dzip = lambda k, v: dict(zip(k, v))
        initiate_table = lambda v: dzip([str(i) for i in range(1, num_servers+1)], [v]*(num_servers+1))

        self.node_table = {str(id): initiate_table(math.inf) for id in range(1, num_servers+1)}
        self.node_hops = {str(id): initiate_table(None) for id in range(1, num_servers+1)}

        print('connecting to neighbors')
        self.neighbors = {str(id): Peer(addrs=servers[id]) for id in neighbors.keys()}

        for idx, c in enumerate(neighbors):
            self.node_table[self.myid][str(idx)] = c
            self.node_hops[self.myid][str(idx)] = self.myid

        Peer.state = self

        TimedFunc(self.step, float(update_interval))
        print('server: success')

    def update(self, server1, server2, cost):

        if not self.server_running:
            print('update: server is not running')
            return

        if cost == 'inf':
            cost = math.inf

        pass

    def step(self):
        '''update node table here'''

        if not self.server_running:
            print('step: server is not running')
            return

        pass

    def packets(self):
        '''Display the number of distance vector (packets) this  server
        has  received  since  the  last  invocation of this information'''

        if not self.server_running:
            print('packets: server is not running')
            return

        pass

    def display(self):
        '''Display the current routing table formatted as a sequence
        of lines, with each line indicating: <source-server-ID> <next-hop-server-ID> <cost-of-path>'''

        if not self.server_running:
            print('display: server is not running')
            return

        pass

    def disable(self, server):
        '''Closes the connection with the given server id'''

        if not self.server_running:
            print('disable: server is not running')
            return

        if server not in self.neighbors.keys():
            print(f'disable: server number {server} is not in neighbor list')
            return

        self.neighbors[server].sock.close()
        del self.neighbors[server];

        self.node_table[self.myid][server] = math.inf
        self.node_hops[self.myid][server] = None

        print('disable: success')

    def crash(self):
        '''Closes all server connections. The neighboring servers must
        handle this close correctly and set the link cost to infinity.'''

        for id, p in self.neighbors.items():
            disable(self, id)

        print('crash: success')


if __name__ == "__main__":
    DVR()

