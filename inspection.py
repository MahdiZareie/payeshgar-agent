import time
from datetime import datetime
from queue import Queue
from payeshgar_http_client.v1.client import PayeshgarServerHTTPClient


class Inspector:
    def __init__(self, queue: Queue, client: PayeshgarServerHTTPClient, groups):
        self.queue = queue
        self.client = client
        self.groups = groups

    _end_points = None

    def _get_endpoint_info(self, id):
        if self._end_points is None:
            endpoint_list = self.client.get_endpoints(self.groups)
            self._end_points = {ep['id']: ep for ep in endpoint_list}
        return self._end_points.get(id)

    def _get_inspections(self):
        inspections = self.client.get_inspections(self.groups, after=datetime.utcnow())  # TODO  pagination
        for inspection in inspections:
            inspection['endpoint'] = self._get_endpoint_info(inspection['endpoint'])
            yield inspection

    def _perform_inspection(self, inspection):
        result = {
            "service_info": inspection,
            "result": {
                "status_code": 200,
                "connect_time": 0.01,
                "response_time": 0.12,
            }
        }
        self.queue.put(result)

    def run(self):
        time.sleep(1)
        for inspection in self._get_inspections():
            self._perform_inspection(inspection)
