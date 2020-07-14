import time
from queue import Queue
from threading import Thread
from config import AgentInfo, Server
from inspection import Inspector
from reporting import Reporter
from payeshgar_http_client.v1.client import PayeshgarServerHTTPClient
from payeshgar_http_client.v1.models import AgentDTO


class Application:
    def __init__(self, agent_info: AgentInfo, server_info: Server):
        self.agent_info = agent_info
        self.server = server_info
        self.queue = Queue()
        self.time_to_go = False
        self.client = PayeshgarServerHTTPClient(base_url=server_info.base_url, token=server_info.token)

    def _introduce_agent(self):
        dto = AgentDTO(name=self.agent_info.name, country=self.agent_info.country, groups=self.server.groups)
        self.client.introduce_agent(dto)

    def _inspection(self):
        inspector = Inspector(self.queue, self.client, self.server.groups)
        while not self.time_to_go:
            inspector.run()
            time.sleep(1)

    def _reporting(self):
        reporter = Reporter(queue=self.queue, client=self.client)
        while not self.time_to_go:
            reporter.run()
            time.sleep(1)

    def run(self):
        self._introduce_agent()
        inspection_thread = Thread(name="inspection", target=self._inspection)
        inspection_thread.start()
        reporting_thread = Thread(name="reporting", target=self._reporting)
        reporting_thread.start()

    def stop(self):
        self.time_to_go = True
