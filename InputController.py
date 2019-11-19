import asyncio
from threading import Thread
import sys

class InputController():

    def __init__(self, dvr):
        self.dvr = dvr
        self.thread = Thread(target = self.handle_input)
        self.thread.start()
        pass

    def parse_command(self, msg):
        args = msg.split()
        try:
            command = getattr(self.dvr, args[0])
        except:
            print(f'Invalid command: "{args[0]}" with args: {args[1:]}')
            command = lambda *args: args # do nothing
        command(*args[1:])

    def handle_input(self):
        '''Waits for stdin then passes to control to a command parser'''
        while True:
            line = sys.stdin.readline()
            self.parse_command(line)

