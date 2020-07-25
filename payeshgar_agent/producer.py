import time
from threading import Thread

from payeshgar_agent.agent import Agent


class Producer(Thread):
    def __init__(self, context: Agent):
        self.context = context
        super(Producer, self).__init__()

    def start_producing(self):
        self.start()

    def run(self):
        while True:
            time.sleep(0.5)
            print("producing")


if __name__ == "__main__":
    from payeshgar_agent.initializer import AgentInitializer

    init = AgentInitializer(dict())
