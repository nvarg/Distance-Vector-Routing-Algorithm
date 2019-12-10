import math
import json
from InputController import InputController
from TimedFunc import TimedFunc
from PeerServer import PeerServer
from threading import Timer

class DVR():

    def __init__(self):

        self.server_running = False
        self.socket = None
        self.packet = 0
        self.myid = None
        self.node_table = None
        self.cost_table = None
        self.servers = None
        self.neighbors = None
        self.neighbor_timers = None
        self.updated = False
        self.interval = None

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
                neighbors[neighbor] = float(cost)

        me = servers[myid]
        sock = PeerServer(*me, self).socket

        dzip = lambda k, v: dict(zip(k, v))
        initiate_table = lambda v: dzip([str(i) for i in range(1, num_servers+1)], [v]*(num_servers+1))

        node_table = {str(id): initiate_table(math.inf) for id in list(neighbors.keys()) + [myid]}

        node_table[myid][myid] = 0
        for to, c in neighbors.items():
            node_table[myid][to] = c

        self.neighbor_timers = {k:Timer(math.inf, self.disable, k) for k in neighbors}
        self.interval = float(update_interval)
        self.myid = myid
        self.node_table = node_table
        self.cost_table = neighbors
        self.servers = servers
        self.neighbors = {k:v for k,v in servers.items() if k in neighbors}
        self.socket = sock
        #TimedFunc(self.step, float(update_interval))
        self.server_running = True
        print('server: success')

    def update(self, server1, server2, cost):

        if not self.server_running:
            print('update: server is not running')
            return

        if server1 != self.myid:
            print('update: cannot update the cost for a server that is not you')
            return

        if server2 not in self.neighbors:
            print('update: cannot update the cost of a link you are not connected to')
            return

        if cost == 'inf':
            cost = math.inf

        self.cost_table[server2] = float(cost)

        print(self.cost_table)

        self.updated = True
        print('update: success')

    def step(self):
        '''update node table here'''

        if not self.server_running:
            print('step: server is not running')
            return

        node_vect = {'vect':self.node_table[self.myid], 'updated': self.updated}
        packet = json.dumps(node_vect).encode('utf-8')

        for addrs in self.neighbors.values():
            self.socket.sendto(packet, addrs)

        if self.updated:
            self.updated = False

        print('step: success')


    def packets(self):
        '''Display the number of distance vector (packets) this  server
        has  received  since  the  last  invocation of this information'''

        if not self.server_running:
            print('packets: server is not running')
            return

        print(f'packets: {self.packet} packets received.')
        self.packet = 0
        print('packets: success')

    def display(self):
        '''Display the current routing table formatted as a sequence
        of lines, with each line indicating: <source-server-ID> <next-hop-server-ID> <cost-of-path>'''

        if not self.server_running:
            print('display: server is not running')
            return

        print(' '.ljust(6) + 'to')
        header = '|'.join(str(i).ljust(6) for i in ['from'] + list(self.servers.keys()))
        print(header)
        print(*(['-']*len(header)), sep='')
        for k,d in self.node_table.items():
            print('|'.join(str(i).ljust(6) for i in [str(k)] + list(d.values())))

        print('display: success')


    def disable(self, server):
        '''Closes the connection with the given server id'''

        if not self.server_running:
            print('disable: server is not running')
            return

        if server not in self.neighbors:
            print(f'disable: server {server} is not in neighbor list')
            return

        del self.neighbors[server];
        del self.cost_table[server];
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

