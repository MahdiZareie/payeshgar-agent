import time
from queue import Queue


class Inspector:
    def __init__(self, queue: Queue):
        self.queue = queue

    def _get_service_definitions(self):
        sample_result = [
            {
                "id": "foo",
                "hostname": "google.com",
                "port": 443,
                "protocol": "https",

            }
        ]
        yield sample_result * 100
        yield sample_result * 100
        yield sample_result * 50

    def _inspect_service(self, service_info):
        # print("inspecting service: {}".format(service_info))
        result = {
            "service_info": service_info,
            "result": {
                "status_code": 200,
                "connect_time": 0.01,
                "response_time": 0.12,
            }
        }
        self.queue.put(result)

    def run(self):
        time.sleep(1)
        for services in self._get_service_definitions():
            for service in services:
                self._inspect_service(service)
            time.sleep(2)
