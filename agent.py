from queue import Queue
from typing import List

from producer import Producer
from consumer import Consumer
from repository.repository_factory import RepositoryFactory


class Agent:
    """
    This class represents an agent instance, it contains require context for inspecting endpoint status
    and reporting those status to a management server

    """
    def __init__(self, groups: List[str], repository_factory: RepositoryFactory):
        self.groups = groups
        self.repository_factory = repository_factory
        self.queue = Queue()
        self.time_to_go = False

    def run(self):
        """
        Spawn producer and consumer threads and return immediately
        """
        Producer(context=self).start_producing()
        Consumer(context=self).start_consuming()

    def stop(self):
        """
        Child threads reads time_to_go flag periodically, and will terminate if it gets true
        """
        self.time_to_go = True
