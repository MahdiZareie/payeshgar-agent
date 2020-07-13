import time
from queue import Queue
from threading import Thread

from inspection import Inspector
from reporting import Reporter


class Application:
    def __init__(self):
        self.queue = Queue()
        self.time_to_go = False

    def _inspection(self):
        inspector = Inspector(self.queue)
        while not self.time_to_go:
            time.sleep(1)
            inspector.run()

    def _reporting(self):
        reporter = Reporter(self.queue)
        while not self.time_to_go:
            time.sleep(1)
            reporter.run()

    def run(self):
        inspection_thread = Thread(name="inspection", target=self._inspection)
        inspection_thread.start()
        reporting_thread = Thread(name="reporting", target=self._reporting)
        reporting_thread.start()

    def stop(self):
        self.time_to_go = True
