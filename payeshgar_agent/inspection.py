from datetime import datetime, timedelta
from queue import Queue

import requests
from dateutil.parser import parse

from payeshgar_agent.payeshgar_http_client.v1.client import PayeshgarServerHTTPClient


class Inspector:
    """
    Inspector is technically a Producer, it perform a
    """

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
        neighborhood = 3  # seconds
        current_time = datetime.utcnow()
        inspections = self.client.get_inspections(self.groups, after=current_time,
                                                  before=current_time + timedelta(seconds=5))  # TODO  pagination

        for inspection in inspections:
            if abs((parse(inspection['timestamp']) - current_time).total_seconds()) > neighborhood:
                break
            inspection['endpoint'] = self._get_endpoint_info(inspection['endpoint'])
            yield inspection

    def _perform_inspection(self, inspection):

        endpoint_detail = inspection['endpoint']['http_details']
        protocol = "https" if endpoint_detail['tls'] else 'http'
        url = "{protocol}://{hostname}:{port}{path}".format(
            protocol=protocol,
            hostname=endpoint_detail['hostname'],
            port=endpoint_detail['port'],
            path=endpoint_detail['path']

        )
        timeout = endpoint_detail['maximum_expected_timeout']
        import time
        before = time.time()
        response = requests.request(endpoint_detail['method_name'], url, timeout=timeout)
        after = time.time()
        self.queue.put(
            {
                'inspection': inspection['id'],
                'connection_status': "SUCCEED",
                'status_code': response.status_code,
                'response_time': round(after - before, 3),
                'byte_received': len(response.content)
            }
        )

    def run(self):
        for inspection in self._get_inspections():
            self._perform_inspection(inspection)
