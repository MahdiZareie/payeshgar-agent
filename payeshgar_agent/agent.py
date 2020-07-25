from queue import Queue
from typing import List




class Agent:
    """
    This class represents an agent instance, it contains require context for inspecting endpoint status
    and reporting those status to a management server

    """

    def __init__(self, groups: List[str], client):
        self.groups = groups
        self.client = client
        self.queue = Queue()
        self.time_to_go = False

    def run(self):
        """
        Spawn producer and consumer threads and return immediately
        """
        from payeshgar_agent.producer import Producer
        from payeshgar_agent.consumer import Consumer
        Producer(context=self).start_producing()
        Consumer(context=self).start_consuming()

    def stop(self):
        """
        Child threads reads time_to_go flag periodically, and will terminate if it gets true
        """
        self.time_to_go = True
