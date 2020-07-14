from threading import Thread


class Producer(Thread):
    def __init__(self, context):
        self.context = context
        super(Producer, self).__init__()

    def start_producing(self):
        self.start()
