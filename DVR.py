import math
import json

from InputController import InputController
from TimedFunc import TimedFunc
from PeerServer import PeerServer

class DVR():

    def __init__(self):

        self.server_running = False
        self.socket = None
        self.packets = 0
        self.myid = None
        self.node_table = None
        self.servers = None
        self.neighbors = None

        InputController(self)

    def __del__(self):
        self.crash()

    def server(self, _t, filename, _i, update_interval):
        '''Reads the topology file, initiates the node table, and starts the update & server thread'''

        if self.server_running:
            print('server: server was started, but it was already running.')
            return

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
                myid, neighbor, cost = line.split()
                neighbors[neighbor] = int(cost)

        me = servers[myid]
        sock = PeerServer(*me, self).socket

        dzip = lambda k, v: dict(zip(k, v))
        initiate_table = lambda v: dzip([str(i) for i in range(1, num_servers+1)], [v]*(num_servers+1))

        node_table = {str(id): initiate_table(math.inf) for id in range(1, num_servers+1)}

        node_table[myid][myid] = 0
        for to, c in neighbors.items():
            node_table[myid][to] = c

        self.myid = myid
        self.node_table = node_table
        self.servers = servers
        self.neighbors = {k:v for k,v in servers.items() if k in neighbors}
        self.socket = sock
        TimedFunc(self.step, float(update_interval))
        self.server_running = True
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

        src = self.socket.getsockname()
        node_vect = self.node_table[self.myid]
        packet = json.dumps(node_vect).encode('utf-8')

        for addrs in self.neighbors.values():
            self.socket.sendto(packet, addrs)
        print('step: success')


    def packets(self):
        '''Display the number of distance vector (packets) this  server
        has  received  since  the  last  invocation of this information'''

        if not self.server_running:
            print('packets: server is not running')
            return

        print(f'packets: {self.packets} packets received.')
        self.packets = 0
        print('packets: success')

    def display(self):
        '''Display the current routing table formatted as a sequence
        of lines, with each line indicating: <source-server-ID> <next-hop-server-ID> <cost-of-path>'''

        if not self.server_running:
            print('display: server is not running')
            return

        for row in self.node_table.values():
            print(*row.values())

    def disable(self, server):
        '''Closes the connection with the given server id'''

        if not self.server_running:
            print('disable: server is not running')
            return

        if server not in self.neighbors:
            print(f'disable: server {server} is not in neighbor list')
            return

        del self.neighbors[server];
        self.node_table[self.myid][server] = math.inf

        print('disable: success')

    def crash(self):
        '''Closes all server connections. The neighboring servers must
        handle this close correctly and set the link cost to infinity.'''

        for id in self.neighbors.copy():
            self.disable(id)

        print('crash: success')


if __name__ == "__main__":
    DVR()

