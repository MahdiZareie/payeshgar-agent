import random
import time
from queue import Queue


class Reporter:
    def __init__(self, queue: Queue):
        self.queue = queue

    def _get_next_batch(self):
        queue_size = self.queue.qsize()
        if queue_size:
            batch = [0] * queue_size
            for i in range(0, queue_size):
                batch[i] = self.queue.get()
            return batch
        return []

    def _submit_batch(self, batch):
        time.sleep(1)
        if random.randint(0, 2) % 2 == 0:
            time.sleep(3)

    def run(self):
        time.sleep(2)
        next_batch = self._get_next_batch()
        if next_batch:
            self._submit_batch(next_batch)
