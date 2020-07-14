import time
from queue import Queue
from threading import Thread

from config import AgentInfo, Server
from inspection import Inspector
from reporting import Reporter


class Application:
    def __init__(self, agent_info: AgentInfo, server_info: Server):
        self.agent_info = agent_info
        self.server = server_info
        self.queue = Queue()
        self.time_to_go = False

    def _inspection(self):
        inspector = Inspector(self.queue)
        while not self.time_to_go:
            inspector.run()
            time.sleep(1)


    def _reporting(self):
        reporter = Reporter(self.queue)
        while not self.time_to_go:
            reporter.run()
            time.sleep(1)


    def run(self):
        inspection_thread = Thread(name="inspection", target=self._inspection)
        inspection_thread.start()
        reporting_thread = Thread(name="reporting", target=self._reporting)
        reporting_thread.start()

    def stop(self):
        self.time_to_go = True
