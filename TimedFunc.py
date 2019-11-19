import time
from threading import Thread

class TimedFunc():

    def __init__(self, func, delay, *args):
        self.thread = Thread(target=self.periodic_update, args=(func, delay, *args))
        self.thread.start()

    def periodic_update(self, func, delay, *args):
        while True:
            time.sleep(delay)
            func(*args)

