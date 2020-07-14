from threading import Thread


class Consumer(Thread):
    def __init__(self, context):
        self.context = context
        super(Consumer, self).__init__()

    def start_consuming(self):
        self.start()
