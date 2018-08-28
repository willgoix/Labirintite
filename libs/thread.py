from threading import Thread
from time import sleep


class ThreadRepeat(Thread):

    def __init__(self, repeatFunction, delay = 0):
        Thread.__init__(self)
        self.repeatFunction = repeatFunction
        self.delay = delay
        self.running = True
        self.daemon = True

    def run(self):
        while self.running:
            self.repeatFunction()

            if self.delay > 0:
                sleep(self.delay)

    def stop(self):
        self.running = False