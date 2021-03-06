from queue import Queue
from payeshgar_agent.payeshgar_http_client.v1.client import PayeshgarServerHTTPClient


class Reporter:
    """
    Each reporter object is a consumer, it reads a batch of inspections-results from a queue, and
    send them to an API

    """
    def __init__(self, queue: Queue, client: PayeshgarServerHTTPClient):
        self.queue = queue  # <-- To read results from
        self.client = client  # <-- To send results to

    def _get_next_batch(self):
        queue_size = self.queue.qsize()
        if queue_size:
            batch = [0] * queue_size
            for i in range(0, queue_size):
                batch[i] = self.queue.get()
            return batch
        return []

    def _submit_batch(self, batch):
        self.client.submit_results(batch)

    def run(self):
        next_batch = self._get_next_batch()
        if next_batch:
            self._submit_batch(next_batch)
